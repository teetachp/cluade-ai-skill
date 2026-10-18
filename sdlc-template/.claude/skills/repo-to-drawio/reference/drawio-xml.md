# draw.io XML quick reference

Use this when hand-writing or editing `.drawio` XML beyond what `graph2drawio.py` produces.

## Skeleton

```xml
<mxfile host="app.diagrams.net">
  <diagram name="Page-1" id="d1">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" page="1" pageWidth="1169" pageHeight="827" adaptiveColors="auto">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- cells go here (remove this comment in real files: no XML comments) -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

Rules: every cell has a unique `id`; vertices have `vertex="1"` and an `<mxGeometry x y width height as="geometry"/>`; edges have `edge="1"`, `source`, `target` and always a child `<mxGeometry relative="1" as="geometry"/>`; put `html=1` in every style; XML-escape HTML inside `value` (`&lt;br&gt;`); no XML comments; no hand-made waypoints.

## Grid

Column x = `col * 180 + 40`, row y = `row * 120 + 40`. Rectangles 140×60, diamonds 160×90, circles 60×60, cylinders 100×70. Main path down one column; branches in the next column at the row of their decision; loop targets in the same column as their source.

## Shapes

| Role | style |
|---|---|
| Step / service | `rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;` |
| Decision | `rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;` |
| Start / end | `ellipse;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;` |
| Database | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#d5e8d4;strokeColor=#82b366;` |
| External system | `rounded=0;whiteSpace=wrap;html=1;dashed=1;fillColor=#ffe6cc;strokeColor=#d79b00;` |
| Queue / topic | `shape=process;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;` |
| Error | `rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;` |
| Note | `shape=note;whiteSpace=wrap;html=1;size=14;align=left;fillColor=#fff2cc;strokeColor=#d6b656;` |
| Title | `text;html=1;align=left;fontSize=20;fontStyle=1;` |
| Actor | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;` 30×60 |

Colors by role: blue steps, green success/data, yellow decisions/notes, orange external/waiting, red errors, purple `#e1d5e7`/`#9673a6` security.

## Edges

| Kind | style |
|---|---|
| Flow | `edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;` |
| Async / event | add `dashed=1;` |
| No arrowhead (org chart, cable) | `endArrow=none;` |
| ER relation | `edgeStyle=entityRelationEdgeStyle;html=1;startArrow=ERmandOne;endArrow=ERmany;` |
| UML inheritance | `endArrow=block;endFill=0;` |
| State transition | no edgeStyle, `endArrow=open;endSize=10;html=1;` |

Edge labels: 1–3 words in `value`; `fontColor=#2D7600` for yes/success, `#B20000` for no/failure.

## Containers

```xml
<mxCell id="svc" value="Order service" style="swimlane;startSize=26;html=1;fillColor=#f5f5f5;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="400" height="240" as="geometry"/>
</mxCell>
<mxCell id="api" value="REST API" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="svc">
  <mxGeometry x="20" y="40" width="140" height="60" as="geometry"/>
</mxCell>
```

Children use coordinates relative to the container. An edge's `parent` is the innermost container holding both endpoints, else `"1"`.

Swimlanes (one per role/service): `swimlane;horizontal=0;startSize=110;html=1;fillColor=#f5f5f5;` stacked at `y = lane * 150`, height 150; children at `x = 120 + col * 180`, `y = 45`; cross-lane edges `parent="1"`.

## ER tables

Table = `swimlane;fontStyle=1;childLayout=stackLayout;horizontalStack=0;resizeParent=1;resizeParentMax=0;horizontal=1;startSize=26;collapsible=0;html=1;` 200 wide; each column a child `text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;html=1;` at `y = 26 + i*26`, height 26, value like `PK id` / `FK order_id`. Relation edges connect the FK row cell to the PK row cell with `entityRelationEdgeStyle` and crow's-foot arrows (`ERmandOne`, `ERone`, `ERzeroToOne`, `ERmany`, `ERzeroToMany`, `ERoneToMany`).

## Themes

Professional: `fontFamily=Inter;fontColor=#0F172A;rounded=1;arcSize=12;` steps `#EFF6FF`/`#2563EB`. Minimal: black and white, `fontFamily=Helvetica`. Dark: `background="#0F172A" adaptiveColors="none"` on mxGraphModel, `fontColor=#F1F5F9`, steps `#1E293B`/`#60A5FA`. Hand-drawn: `sketch=1;curveFitting=1;jiggle=2;` on every cell.

Full style reference: https://github.com/jgraph/drawio-mcp/blob/main/shared/style-reference.md
