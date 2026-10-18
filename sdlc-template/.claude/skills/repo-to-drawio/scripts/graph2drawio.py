#!/usr/bin/env python3
"""Turn a small JSON graph description into a draw.io (.drawio) file.

Usage:
    graph2drawio.py graph.json -o docs/diagrams/flow.drawio
    graph2drawio.py graph.json --stdout

Input JSON:
{
  "title": "Order flow",
  "direction": "TB",              # TB (top-down, default) or LR (left-right)
  "layout": "layered",            # layered (default) or swimlane (one lane per group)
  "nodes": [
    {"id": "start", "label": "Request", "type": "start"},
    {"id": "auth",  "label": "Auth middleware", "type": "process", "group": "API", "note": "JWT"},
    {"id": "ok",    "label": "Valid token?", "type": "decision", "group": "API"},
    {"id": "db",    "label": "orders table", "type": "datastore", "group": "Data"},
    {"id": "err",   "label": "401", "type": "error"}
  ],
  "edges": [
    {"from": "start", "to": "auth"},
    {"from": "auth", "to": "ok"},
    {"from": "ok", "to": "db", "label": "yes"},
    {"from": "ok", "to": "err", "label": "no", "style": "error"},
    {"from": "db", "to": "auth", "style": "async"}
  ]
}

Node types: start, end, process, decision, datastore, external, queue, error, note.
Edge styles: default, async (dashed), error (red), data (green).
Layout is a simple layered (Sugiyama-style) placement on draw.io's 180x120 grid.
Only the standard library is used.
"""
import argparse
import json
import sys
from collections import defaultdict
from xml.sax.saxutils import escape

COL = 180
ROW = 120
MARGIN = 40

NODE_STYLES = {
    "process":   ("rounded=1;whiteSpace=wrap;html=1;fontSize=14;fillColor=#dae8fc;strokeColor=#6c8ebf;", 140, 60),
    "start":     ("ellipse;whiteSpace=wrap;html=1;fontSize=14;fillColor=#d5e8d4;strokeColor=#82b366;", 120, 60),
    "end":       ("ellipse;whiteSpace=wrap;html=1;fontSize=14;fillColor=#d5e8d4;strokeColor=#82b366;", 120, 60),
    "decision":  ("rhombus;whiteSpace=wrap;html=1;fontSize=14;fillColor=#fff2cc;strokeColor=#d6b656;", 160, 90),
    "datastore": ("shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fontSize=14;fillColor=#d5e8d4;strokeColor=#82b366;", 110, 70),
    "external":  ("rounded=0;whiteSpace=wrap;html=1;dashed=1;fontSize=14;fillColor=#ffe6cc;strokeColor=#d79b00;", 140, 60),
    "queue":     ("shape=process;whiteSpace=wrap;html=1;fontSize=14;fillColor=#ffe6cc;strokeColor=#d79b00;", 140, 60),
    "error":     ("rounded=1;whiteSpace=wrap;html=1;fontSize=14;fillColor=#f8cecc;strokeColor=#b85450;", 140, 60),
    "note":      ("shape=note;whiteSpace=wrap;html=1;size=14;fontSize=12;align=left;spacingLeft=6;fillColor=#fff2cc;strokeColor=#d6b656;", 160, 70),
}

EDGE_STYLES = {
    "default": "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;",
    "async":   "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;dashed=1;",
    "error":   "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#b85450;fontColor=#B20000;",
    "data":    "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#82b366;fontColor=#2D7600;",
}

LANE_FILLS = ["#f5f5f5", "#e8f4f8", "#fff0e6", "#e8f5e9", "#fff9e6", "#fce4ec"]


def label_html(node):
    text = escape(node["label"])
    if node.get("note"):
        text += "&lt;br&gt;&lt;small&gt;" + escape(node["note"]) + "&lt;/small&gt;"
    return text.replace("<", "&lt;").replace(">", "&gt;") if "<" in text else text


def assign_layers(nodes, edges):
    """Longest-path layering. Back edges (found by DFS) are ignored for layering."""
    ids = [n["id"] for n in nodes]
    out = defaultdict(list)
    for e in edges:
        out[e["from"]].append(e["to"])
    state = {}
    back = set()

    def dfs(u):
        state[u] = 1
        for v in out[u]:
            if state.get(v) == 1:
                back.add((u, v))
            elif v not in state:
                dfs(v)
        state[u] = 2

    sys.setrecursionlimit(max(1000, len(ids) * 4))
    for u in ids:
        if u not in state:
            dfs(u)

    fwd = [(e["from"], e["to"]) for e in edges if (e["from"], e["to"]) not in back]
    indeg = {i: 0 for i in ids}
    succ = defaultdict(list)
    for a, b in fwd:
        succ[a].append(b)
        indeg[b] += 1
    layer = {i: 0 for i in ids}
    queue = [i for i in ids if indeg[i] == 0]
    while queue:
        u = queue.pop(0)
        for v in succ[u]:
            layer[v] = max(layer[v], layer[u] + 1)
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    return layer


def order_in_layers(nodes, edges, layer):
    """One barycenter pass to reduce crossings."""
    pred = defaultdict(list)
    for e in edges:
        pred[e["to"]].append(e["from"])
    layers = defaultdict(list)
    for n in nodes:
        layers[layer[n["id"]]].append(n["id"])
    pos = {}
    for l in sorted(layers):
        if l == 0:
            ordered = layers[l]
        else:
            def key(i):
                ps = [pos[p] for p in pred[i] if p in pos]
                return sum(ps) / len(ps) if ps else 1e9
            ordered = sorted(layers[l], key=key)
        for idx, i in enumerate(ordered):
            pos[i] = idx
    return pos, layers


def build(graph):
    nodes = graph["nodes"]
    edges = graph.get("edges", [])
    direction = graph.get("direction", "TB").upper()
    layout = graph.get("layout", "layered")
    by_id = {n["id"]: n for n in nodes}
    for e in edges:
        for k in ("from", "to"):
            if e[k] not in by_id:
                raise SystemExit(f"edge references unknown node: {e[k]}")

    layer = assign_layers(nodes, edges)
    pos, layers = order_in_layers(nodes, edges, layer)

    cells = []
    nid = [10]

    def next_id():
        nid[0] += 1
        return f"c{nid[0]}"

    def vertex(cid, value, style, x, y, w, h, parent="1"):
        cells.append(
            f'<mxCell id="{cid}" value="{value}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )

    title_h = 60 if graph.get("title") else 0
    coords = {}  # id -> (x, y, w, h, parent)

    if layout == "swimlane":
        groups = []
        for n in nodes:
            g = n.get("group", "Other")
            if g not in groups:
                groups.append(g)
        max_layer = max(layer.values()) if layer else 0
        lane_w = (max_layer + 1) * COL + 300
        lane_h = ROW + 30
        # several nodes of one group in one layer stack vertically
        slot = defaultdict(int)
        lane_rows = defaultdict(int)
        for n in nodes:
            k = (n.get("group", "Other"), layer[n["id"]])
            slot[n["id"]] = lane_rows[k]
            lane_rows[k] += 1
        lane_depth = {g: max([lane_rows[(gg, l)] for (gg, l) in lane_rows if gg == g] or [1]) for g in groups}
        y = title_h
        lane_ids = {}
        for gi, g in enumerate(groups):
            h = lane_depth[g] * ROW + 30
            lid = f"lane{gi}"
            lane_ids[g] = lid
            vertex(lid, escape(g), f"swimlane;horizontal=0;startSize=110;html=1;fontSize=14;fillColor={LANE_FILLS[gi % len(LANE_FILLS)]};", 0, y, lane_w, h)
            for n in nodes:
                if n.get("group", "Other") != g:
                    continue
                style, w, hh = NODE_STYLES.get(n.get("type", "process"), NODE_STYLES["process"])
                x = 120 + layer[n["id"]] * COL
                ny = 45 + slot[n["id"]] * ROW
                coords[n["id"]] = (x, ny, w, hh, lid)
                vertex(n["id"], label_html(n), style, x, ny, w, hh, lid)
            y += h
        width, height = lane_w, y
    else:
        for n in nodes:
            style, w, h = NODE_STYLES.get(n.get("type", "process"), NODE_STYLES["process"])
            l, p = layer[n["id"]], pos[n["id"]]
            if direction == "LR":
                x, y = MARGIN + l * COL, MARGIN + title_h + p * ROW
            else:
                x, y = MARGIN + p * COL, MARGIN + title_h + l * ROW
            coords[n["id"]] = (x, y, w, h, "1")

        # group containers: bounding box of their members, drawn behind the nodes
        groups = defaultdict(list)
        for n in nodes:
            if n.get("group"):
                groups[n["group"]].append(n["id"])
        group_ids = {}
        for gi, (g, members) in enumerate(groups.items()):
            xs = [coords[m][0] for m in members]
            ys = [coords[m][1] for m in members]
            xe = [coords[m][0] + coords[m][2] for m in members]
            ye = [coords[m][1] + coords[m][3] for m in members]
            gx, gy = min(xs) - 20, min(ys) - 40
            gw, gh = max(xe) - gx + 20, max(ye) - gy + 20
            gid = f"grp{gi}"
            group_ids[g] = (gid, gx, gy)
            vertex(gid, escape(g), f"swimlane;startSize=26;html=1;fontSize=14;fontStyle=1;fillColor={LANE_FILLS[gi % len(LANE_FILLS)]};strokeColor=#999999;pointerEvents=0;", gx, gy, gw, gh)
        for n in nodes:
            x, y, w, h, _ = coords[n["id"]]
            parent = "1"
            if n.get("group"):
                gid, gx, gy = group_ids[n["group"]]
                parent, x, y = gid, x - gx, y - gy
            coords[n["id"]] = (x, y, w, h, parent)
            style, _, _ = NODE_STYLES.get(n.get("type", "process"), NODE_STYLES["process"])
            vertex(n["id"], label_html(n), style, x, y, w, h, parent)
        all_x = [MARGIN + p * COL + 160 for p in pos.values()]
        width = max(all_x) + MARGIN if all_x else 400
        height = MARGIN + title_h + (max(layer.values()) + 1) * ROW + MARGIN if layer else 300

    if graph.get("title"):
        vertex("title", escape(graph["title"]), "text;html=1;align=left;verticalAlign=middle;fontSize=20;fontStyle=1;", MARGIN, 10, 600, 40)

    for e in edges:
        style = EDGE_STYLES.get(e.get("style", "default"), EDGE_STYLES["default"])
        src_parent, dst_parent = coords[e["from"]][4], coords[e["to"]][4]
        parent = src_parent if src_parent == dst_parent else "1"
        cells.append(
            f'<mxCell id="{next_id()}" value="{escape(e.get("label", ""))}" style="{style}" edge="1" parent="{parent}" '
            f'source="{e["from"]}" target="{e["to"]}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )

    name = escape(graph.get("title", "Diagram"))
    return (
        '<mxfile host="graph2drawio" version="1">'
        f'<diagram name="{name}" id="d1">'
        f'<mxGraphModel dx="{width}" dy="{height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" '
        'fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0" adaptiveColors="auto">'
        '<root><mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("graph", help="JSON graph file")
    ap.add_argument("-o", "--output", help="output .drawio path")
    ap.add_argument("--stdout", action="store_true")
    a = ap.parse_args()
    with open(a.graph, encoding="utf-8") as f:
        graph = json.load(f)
    xml = build(graph)
    if a.stdout or not a.output:
        print(xml)
    else:
        import os
        os.makedirs(os.path.dirname(os.path.abspath(a.output)), exist_ok=True)
        with open(a.output, "w", encoding="utf-8") as f:
            f.write(xml)
        print(f"wrote {a.output} ({len(graph['nodes'])} nodes, {len(graph.get('edges', []))} edges)")


if __name__ == "__main__":
    main()
