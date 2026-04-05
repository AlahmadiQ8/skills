#!/usr/bin/env python3
"""
Validate an Obsidian .canvas file against the JSON Canvas 1.0 spec.

Usage:
    python validate_canvas.py <path-to-canvas-file>

Exits 0 on valid, 1 on invalid. Prints all issues found.
"""

import json
import sys
import os
import re

VALID_NODE_TYPES = {"text", "file", "link", "group"}
VALID_SIDES = {"top", "right", "bottom", "left"}
VALID_ENDS = {"none", "arrow"}
VALID_BG_STYLES = {"cover", "ratio", "repeat"}
PRESET_COLORS = {"1", "2", "3", "4", "5", "6"}
HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

GENERIC_NODE_REQUIRED = {"id", "type", "x", "y", "width", "height"}


def is_valid_color(value):
    if value in PRESET_COLORS:
        return True
    if isinstance(value, str) and HEX_COLOR_RE.match(value):
        return True
    return False


def validate_canvas(data):
    issues = []

    if not isinstance(data, dict):
        issues.append("Top level must be a JSON object")
        return issues

    allowed_top = {"nodes", "edges"}
    for key in data:
        if key not in allowed_top:
            issues.append(f"Unknown top-level key: '{key}'")

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    if not isinstance(nodes, list):
        issues.append("`nodes` must be an array")
        nodes = []
    if not isinstance(edges, list):
        issues.append("`edges` must be an array")
        edges = []

    node_ids = set()
    seen_ids = set()

    for i, node in enumerate(nodes):
        prefix = f"nodes[{i}]"
        if not isinstance(node, dict):
            issues.append(f"{prefix}: must be an object")
            continue

        # Check required generic fields
        for field in GENERIC_NODE_REQUIRED:
            if field not in node:
                issues.append(f"{prefix}: missing required field '{field}'")

        nid = node.get("id")
        if nid is not None:
            if nid in seen_ids:
                issues.append(f"{prefix}: duplicate id '{nid}'")
            seen_ids.add(nid)
            node_ids.add(nid)

        # Validate position/size are integers
        for field in ("x", "y", "width", "height"):
            val = node.get(field)
            if val is not None and not isinstance(val, int):
                issues.append(f"{prefix}.{field}: must be an integer, got {type(val).__name__}")

        # Validate width/height are positive
        for field in ("width", "height"):
            val = node.get(field)
            if isinstance(val, int) and val <= 0:
                issues.append(f"{prefix}.{field}: must be positive, got {val}")

        # Validate color
        color = node.get("color")
        if color is not None and not is_valid_color(color):
            issues.append(f"{prefix}.color: invalid color '{color}' — use hex (#RRGGBB) or preset (1-6)")

        ntype = node.get("type")
        if ntype not in VALID_NODE_TYPES:
            issues.append(f"{prefix}.type: invalid type '{ntype}' — must be text, file, link, or group")
            continue

        # Type-specific validation
        if ntype == "text":
            if "text" not in node:
                issues.append(f"{prefix}: text node missing required 'text' field")
            elif not isinstance(node["text"], str):
                issues.append(f"{prefix}.text: must be a string")

        elif ntype == "file":
            if "file" not in node:
                issues.append(f"{prefix}: file node missing required 'file' field")
            elif not isinstance(node["file"], str):
                issues.append(f"{prefix}.file: must be a string")
            subpath = node.get("subpath")
            if subpath is not None:
                if not isinstance(subpath, str):
                    issues.append(f"{prefix}.subpath: must be a string")
                elif not subpath.startswith("#"):
                    issues.append(f"{prefix}.subpath: must start with '#'")

        elif ntype == "link":
            if "url" not in node:
                issues.append(f"{prefix}: link node missing required 'url' field")
            elif not isinstance(node["url"], str):
                issues.append(f"{prefix}.url: must be a string")

        elif ntype == "group":
            label = node.get("label")
            if label is not None and not isinstance(label, str):
                issues.append(f"{prefix}.label: must be a string")
            bg = node.get("background")
            if bg is not None and not isinstance(bg, str):
                issues.append(f"{prefix}.background: must be a string")
            bgs = node.get("backgroundStyle")
            if bgs is not None and bgs not in VALID_BG_STYLES:
                issues.append(f"{prefix}.backgroundStyle: invalid '{bgs}' — must be cover, ratio, or repeat")

    # Validate edges
    edge_ids = set()
    for i, edge in enumerate(edges):
        prefix = f"edges[{i}]"
        if not isinstance(edge, dict):
            issues.append(f"{prefix}: must be an object")
            continue

        for field in ("id", "fromNode", "toNode"):
            if field not in edge:
                issues.append(f"{prefix}: missing required field '{field}'")

        eid = edge.get("id")
        if eid is not None:
            if eid in edge_ids or eid in seen_ids:
                issues.append(f"{prefix}: duplicate id '{eid}'")
            edge_ids.add(eid)
            seen_ids.add(eid)

        # Check node references
        from_node = edge.get("fromNode")
        if from_node is not None and from_node not in node_ids:
            issues.append(f"{prefix}.fromNode: references unknown node '{from_node}'")

        to_node = edge.get("toNode")
        if to_node is not None and to_node not in node_ids:
            issues.append(f"{prefix}.toNode: references unknown node '{to_node}'")

        # Self-loop check
        if from_node is not None and from_node == to_node:
            issues.append(f"{prefix}: self-loop (fromNode == toNode == '{from_node}')")

        # Validate sides
        for field in ("fromSide", "toSide"):
            val = edge.get(field)
            if val is not None and val not in VALID_SIDES:
                issues.append(f"{prefix}.{field}: invalid side '{val}' — must be top, right, bottom, or left")

        # Validate ends
        for field in ("fromEnd", "toEnd"):
            val = edge.get(field)
            if val is not None and val not in VALID_ENDS:
                issues.append(f"{prefix}.{field}: invalid end '{val}' — must be none or arrow")

        # Validate edge color
        color = edge.get("color")
        if color is not None and not is_valid_color(color):
            issues.append(f"{prefix}.color: invalid color '{color}'")

        label = edge.get("label")
        if label is not None and not isinstance(label, str):
            issues.append(f"{prefix}.label: must be a string")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_canvas.py <canvas-file> [--quiet]")
        sys.exit(2)

    path = sys.argv[1]
    quiet = "--quiet" in sys.argv

    if not os.path.exists(path):
        print(f"ERROR: File not found: {path}")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        sys.exit(1)

    issues = validate_canvas(data)

    if issues:
        print(f"INVALID — {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"  ✗ {issue}")
        sys.exit(1)
    else:
        node_count = len(data.get("nodes", []))
        edge_count = len(data.get("edges", []))
        if not quiet:
            types = {}
            for n in data.get("nodes", []):
                t = n.get("type", "unknown")
                types[t] = types.get(t, 0) + 1
            type_summary = ", ".join(f"{v} {k}" for k, v in sorted(types.items()))
            print(f"VALID — {node_count} nodes ({type_summary}), {edge_count} edges")
        sys.exit(0)


if __name__ == "__main__":
    main()
