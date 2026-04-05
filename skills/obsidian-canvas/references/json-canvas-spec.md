# JSON Canvas Spec — v1.0

Source: https://jsoncanvas.org/spec/1.0/

## Top Level

The top level of a `.canvas` file contains two arrays:

- `nodes` (optional, array of nodes)
- `edges` (optional, array of edges)

## Nodes

Nodes are objects within the canvas. Types: `text`, `file`, `link`, `group`.

Nodes are ordered by ascending z-index — first node renders below all others, last node on top.

### Generic Node (all types)

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `id` | yes | string | Unique ID |
| `type` | yes | string | `text`, `file`, `link`, or `group` |
| `x` | yes | integer | X position in pixels |
| `y` | yes | integer | Y position in pixels |
| `width` | yes | integer | Width in pixels |
| `height` | yes | integer | Height in pixels |
| `color` | no | canvasColor | Node color |

### Text Node

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `text` | yes | string | Plain text with Markdown syntax |

### File Node

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `file` | yes | string | Path to file within vault |
| `subpath` | no | string | Link to heading or block (starts with `#`) |

### Link Node

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `url` | yes | string | URL to embed |

### Group Node

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `label` | no | string | Text label for the group |
| `background` | no | string | Path to background image |
| `backgroundStyle` | no | string | `cover`, `ratio`, or `repeat` |

## Edges

Edges connect one node to another.

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `id` | yes | string | Unique ID |
| `fromNode` | yes | string | Source node ID |
| `fromSide` | no | string | `top`, `right`, `bottom`, or `left` |
| `fromEnd` | no | string | `none` or `arrow` (default: `none`) |
| `toNode` | yes | string | Target node ID |
| `toSide` | no | string | `top`, `right`, `bottom`, or `left` |
| `toEnd` | no | string | `none` or `arrow` (default: `arrow`) |
| `color` | no | canvasColor | Line color |
| `label` | no | string | Text label for the edge |

## Color (canvasColor)

Colors are strings, either:
- Hex format: `"#FF0000"`
- Preset number:
  - `"1"` = red
  - `"2"` = orange
  - `"3"` = yellow
  - `"4"` = green
  - `"5"` = cyan
  - `"6"` = purple
