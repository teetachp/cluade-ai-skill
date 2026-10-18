---
name: repo-to-drawio
description: Read a codebase and draw its flows as editable draw.io (.drawio) diagrams: request/data flow, module dependencies, deployment, or a process across services. Use when asked to "draw the flow of this repo", "diagram how X works", "make a draw.io of the architecture", or to produce a .drawio file. For Mermaid in Markdown use mermaid-diagrams; for database schemas use er-diagram.
---

# Repo → draw.io

Produce a diagram a teammate can open and edit in draw.io (desktop, diagrams.net, or the VS Code "Draw.io Integration" extension). The diagram must reflect what the code does, not what the README claims.

## 1. Read before drawing

1. Find the entry points: HTTP routes, CLI commands, cron/queue consumers, `main`.
2. Follow one path end to end: middleware → handler → service → repository/DB → external calls → events.
3. Note the boundaries: modules/packages, services, databases, queues, third-party APIs.
4. Write down every node and edge you will draw with its source file (`src/orders/service.ts:42`). If you cannot point to code for an edge, do not draw it.

Scope to one question per diagram ("how does an order get created?", "which modules depend on `auth`?"). Split large systems into several diagrams rather than one wall.

## 2. Describe the graph as JSON

Write a graph file (keep it in `docs/diagrams/<name>.graph.json` so it can be regenerated later):

```json
{
  "title": "Create order",
  "direction": "TB",
  "layout": "layered",
  "nodes": [
    {"id": "req", "label": "POST /orders", "type": "start"},
    {"id": "auth", "label": "authMiddleware", "type": "process", "group": "API", "note": "src/middleware/auth.ts"},
    {"id": "valid", "label": "Token valid?", "type": "decision", "group": "API"},
    {"id": "svc", "label": "OrderService.create", "type": "process", "group": "API"},
    {"id": "db", "label": "orders", "type": "datastore", "group": "Postgres"},
    {"id": "bus", "label": "order.created", "type": "queue", "group": "Kafka"},
    {"id": "err", "label": "401", "type": "error"},
    {"id": "done", "label": "201 Created", "type": "end"}
  ],
  "edges": [
    {"from": "req", "to": "auth"},
    {"from": "auth", "to": "valid"},
    {"from": "valid", "to": "svc", "label": "yes", "style": "data"},
    {"from": "valid", "to": "err", "label": "no", "style": "error"},
    {"from": "svc", "to": "db", "label": "insert"},
    {"from": "svc", "to": "bus", "style": "async"},
    {"from": "svc", "to": "done"}
  ]
}
```

- `type`: `start`, `end`, `process`, `decision`, `datastore`, `external`, `queue`, `error`, `note`
- `style` on edges: `default`, `async` (dashed), `error` (red), `data` (green)
- `group`: draws a titled container around the members. `layout: "swimlane"` makes one horizontal lane per group instead (good for flows across roles/services).
- `direction`: `TB` or `LR`. Labels: 2–5 words; put the file path or technology in `note`.

## 3. Generate the file

```bash
python3 <skill-dir>/scripts/graph2drawio.py docs/diagrams/create-order.graph.json -o docs/diagrams/create-order.drawio
```

`<skill-dir>` is the directory containing this SKILL.md. The script needs only the Python standard library and does a layered layout on draw.io's grid; a diagram of up to ~30 nodes comes out readable. For more, split the diagram.

Commit both the `.graph.json` and the `.drawio`. To also embed a picture in Markdown, export PNG/SVG from draw.io (`File → Export`), or with the desktop app CLI: `drawio -x -f svg -o docs/diagrams/create-order.svg docs/diagrams/create-order.drawio`.

## If a draw.io MCP tool is available

When the session has a `create_diagram` tool (draw.io MCP), you can show the diagram inline by passing the `<mxGraphModel>…</mxGraphModel>` part of the generated file as `xml` with `routing: "libavoid"`. Still write the `.drawio` file to the repo; the inline view is for review, the file is the deliverable. For hand-placed XML beyond what the script produces, see [reference/drawio-xml.md](reference/drawio-xml.md).

## Report

Give the file path(s), the question the diagram answers, and the list of nodes with their source locations, so a reviewer can verify the diagram against the code. State anything you inferred rather than read.
