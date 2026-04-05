---
name: obsidian-canvas
description: Create and edit Obsidian canvas files (.canvas) — visual spatial layouts that connect notes, text cards, links, images, and groups with edges. Uses the JSON Canvas open format. Use this skill whenever the user mentions canvas, visual mapping, mind map, concept map, flowchart, spatial layout, node graph, connecting notes visually, or wants to create a .canvas file in their Obsidian vault — even if they just say "map out", "visualize my notes", "create a diagram of", or "connect these ideas".
---

# Obsidian Canvas Builder

You create `.canvas` files for Obsidian using the [JSON Canvas](https://jsoncanvas.org/) open format. Canvas files are spatial layouts — nodes placed on an infinite 2D surface, connected by edges. They're great for mind maps, project boards, concept maps, flowcharts, research boards, and any visual arrangement of ideas.

## The Format

A `.canvas` file is JSON with two arrays: `nodes` and `edges`. For the full spec, read `references/json-canvas-spec.md`. Here's the essential structure:

```json
{
  "nodes": [
    {
      "id": "node1",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 120,
      "text": "# My Idea\n\nSome details here"
    }
  ],
  "edges": [
    {
      "id": "edge1",
      "fromNode": "node1",
      "toNode": "node2",
      "toEnd": "arrow"
    }
  ]
}
```

## Node Types

### Text — inline content
```json
{"id": "t1", "type": "text", "x": 0, "y": 0, "width": 250, "height": 140, "text": "# Title\n\nMarkdown content"}
```

### File — reference to a vault note or attachment
```json
{"id": "f1", "type": "file", "x": 300, "y": 0, "width": 250, "height": 400, "file": "Projects/My Project.md"}
```
Optional `subpath` to link to a heading: `"subpath": "#Overview"`

### Link — embedded web page
```json
{"id": "l1", "type": "link", "x": 600, "y": 0, "width": 400, "height": 300, "url": "https://example.com"}
```

### Group — visual container
```json
{"id": "g1", "type": "group", "x": -20, "y": -20, "width": 600, "height": 500, "label": "Phase 1"}
```
Groups contain other nodes spatially — any node whose position falls within the group's bounds is visually inside it. Groups have lower z-index (place them earlier in the `nodes` array so they render behind their children).

## Edges

Edges connect nodes with lines. Minimal edge:
```json
{"id": "e1", "fromNode": "t1", "toNode": "t2"}
```

Full edge with all options:
```json
{
  "id": "e1",
  "fromNode": "t1",
  "fromSide": "right",
  "fromEnd": "none",
  "toNode": "t2",
  "toSide": "left",
  "toEnd": "arrow",
  "color": "4",
  "label": "depends on"
}
```

- `fromSide` / `toSide`: `top`, `right`, `bottom`, `left` — which side of the node the edge connects to. Omit to let Obsidian auto-route.
- `fromEnd` / `toEnd`: `none` or `arrow`. Defaults: `fromEnd` = `none`, `toEnd` = `arrow`.
- `label`: text displayed on the edge.

## Colors

Both nodes and edges accept a `color` field. Values:
- Preset: `"1"` red, `"2"` orange, `"3"` yellow, `"4"` green, `"5"` cyan, `"6"` purple
- Hex: `"#FF5733"`

Use color to encode meaning (status, category, priority) rather than decoration.

---

## Layout Strategy

Good canvas layouts are readable, scannable, and convey structure through spatial arrangement. The layout you choose should match the content's natural structure.

### Choosing a Layout

| Pattern | When to use | Flow direction |
|---------|------------|----------------|
| **Left-to-right flow** | Processes, timelines, pipelines | → |
| **Top-to-bottom flow** | Hierarchies, decision trees | ↓ |
| **Hub-and-spoke** | Central concept with branches | Center out |
| **Grid** | Comparisons, matrices, collections | Rows/cols |
| **Clusters** | Grouped topics, categorized items | Groups |
| **Free-form** | Brainstorming, mixed content | Organic |

### Spacing and Sizing

These defaults produce clean, readable canvases in Obsidian:

- **Standard card**: 250×120 px (title + a few bullets)
- **Detailed card**: 300×200 px (longer content, lists)
- **File embed card**: 250×400 px (note preview)
- **Link embed card**: 400×300 px (web preview)
- **Group padding**: 40px on each side around contained nodes
- **Horizontal gap**: 100px between adjacent nodes
- **Vertical gap**: 80px between rows
- **Row/column alignment**: keep nodes on a consistent grid

For a left-to-right flow with 4 nodes in a row:
```
Node 1: x=0,     y=0
Node 2: x=350,   y=0    (250 width + 100 gap)
Node 3: x=700,   y=0
Node 4: x=1050,  y=0
```

For a top-to-bottom flow:
```
Node 1: x=0, y=0
Node 2: x=0, y=200     (120 height + 80 gap)
Node 3: x=0, y=400
```

### Groups

When grouping nodes:
1. Calculate the bounding box of all nodes in the group
2. Add 40px padding on each side
3. Place the group node **before** its children in the `nodes` array (lower z-index)

```
Group:    x = min_x - 40, y = min_y - 60 (extra top for label), 
          width = (max_x + max_width) - min_x + 80,
          height = (max_y + max_height) - min_y + 100
```

### Edge Routing

- For left-to-right flows: `fromSide: "right"`, `toSide: "left"`
- For top-to-bottom flows: `fromSide: "bottom"`, `toSide: "top"`
- For hub-and-spoke: omit sides (let Obsidian auto-route)
- When in doubt, omit `fromSide`/`toSide` — Obsidian's auto-routing works well

---

## Workflow

### 1. Understand the Request

Identify what the user wants to visualize:
- **Content**: What are the nodes? (ideas, notes, links, topics)
- **Structure**: How do they relate? (linear flow, hierarchy, clusters, free-form)
- **Vault context**: Are there existing notes to reference as file nodes?

### 2. Plan the Layout

Before writing JSON, sketch the layout mentally:
- How many nodes and what types?
- What layout pattern fits?
- Which nodes need edges?
- Should anything be grouped?

### 3. Generate the Canvas

Build the JSON following the spec. Use the `scripts/validate_canvas.py` script to validate:

```bash
python /path/to/skills/obsidian-canvas/scripts/validate_canvas.py <canvas-file>
```

This catches structural errors — missing fields, bad types, dangling edge references, duplicate IDs, etc.

### 4. Save the File

Save to the user's vault as a `.canvas` file:
- Default location: vault root or a folder the user specifies
- Use descriptive names: `project-roadmap.canvas`, `ml-concepts.canvas`

If the Obsidian CLI is available, you can open the canvas after creating it:
```bash
obsidian open path="my-canvas.canvas"
```

---

## ID Generation

Use descriptive, readable IDs that hint at the node's content:

- Text nodes: `"overview"`, `"step-1"`, `"pros-postgres"`
- File nodes: `"note-project-alpha"`, `"file-readme"`
- Link nodes: `"link-github-repo"`, `"link-docs"`
- Group nodes: `"group-phase-1"`, `"group-databases"`
- Edges: `"edge-overview-to-step1"`, `"edge-research-to-design"`

Readable IDs make the JSON easier to understand and debug. Avoid opaque UUIDs or sequential numbers like `"node1"`, `"node2"`.

---

## Common Canvas Patterns

### Flowchart / Process

Left-to-right with labeled edges for transitions:

```
[Idea] --"approved"--> [Design] --"reviewed"--> [Build] --"tested"--> [Ship]
```

### Mind Map

Central topic with spokes radiating outward:

```
                [Subtopic A]
                     ↑
[Subtopic D] ← [Central Topic] → [Subtopic B]
                     ↓
                [Subtopic C]
```

### Comparison Board

Grid layout with groups per category:

```
┌─ Group: Option A ──┐  ┌─ Group: Option B ──┐
│ [Pros]   [Cons]     │  │ [Pros]   [Cons]     │
└─────────────────────┘  └─────────────────────┘
```

### Research Board

Mixed node types — file embeds for existing notes, text cards for annotations, link cards for sources:

```
┌─ Group: Sources ─────────┐
│ [link: Paper 1] [link: 2]│
└──────────────────────────┘
         ↓
┌─ Group: Notes ───────────┐
│ [file: Summary.md]       │
│ [text: Key Insight]      │
└──────────────────────────┘
```

---

## Tips

- **Start simple.** A canvas with 5 well-placed nodes beats 30 cramped ones. You can always suggest the user expand later.
- **Use text nodes for ephemeral content** (brainstorming, annotations) and **file nodes for durable content** (existing vault notes). Text nodes don't show up in backlinks or search.
- **Color-code consistently.** If you use `"4"` (green) for "done" on one node, use it on all "done" nodes.
- **Label edges when the relationship isn't obvious.** "leads to" or "depends on" adds a lot of clarity. Skip labels for obvious sequential flows.
- **Groups are powerful for hierarchy.** A canvas with 20 ungrouped nodes is hard to read. Group by category, phase, or theme.
- **Validate before delivering.** Always run `scripts/validate_canvas.py` on the output. A malformed canvas won't open properly in Obsidian.
