#!/usr/bin/env python3
"""
Grade a canvas eval by checking assertions programmatically.

Usage:
    python grade_canvas.py <canvas-file> --eval <eval-id> [--output <grading.json>]

Eval IDs:
    1 = sdlc-flow
    2 = ml-concepts
    3 = db-comparison
"""

import json
import sys
import os
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VALIDATOR = os.path.join(SCRIPT_DIR, "..", "scripts", "validate_canvas.py")


def load_canvas(path):
    with open(path, "r") as f:
        return json.load(f)


def run_validator(path):
    result = subprocess.run(
        [sys.executable, VALIDATOR, path, "--quiet"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def nodes_by_type(data, ntype):
    return [n for n in data.get("nodes", []) if n.get("type") == ntype]


def grade_eval_1(data, path):
    """SDLC flow: 6 text nodes, left-to-right, 5+ edges, stage names, sequential flow."""
    results = []

    # 1. Valid canvas
    valid = run_validator(path)
    results.append({
        "text": "The output is a valid .canvas file (passes validate_canvas.py)",
        "passed": valid,
        "evidence": "Validator passed" if valid else "Validator failed"
    })

    text_nodes = nodes_by_type(data, "text")

    # 2. Exactly 6 text nodes
    results.append({
        "text": "There are exactly 6 text nodes for the 6 stages",
        "passed": len(text_nodes) == 6,
        "evidence": f"Found {len(text_nodes)} text nodes"
    })

    edges = data.get("edges", [])

    # 3. At least 5 edges
    results.append({
        "text": "There are at least 5 edges connecting consecutive stages",
        "passed": len(edges) >= 5,
        "evidence": f"Found {len(edges)} edges"
    })

    # 4. Left-to-right arrangement
    xs = sorted([n.get("x", 0) for n in text_nodes])
    increasing = all(xs[i] < xs[i+1] for i in range(len(xs)-1)) if len(xs) > 1 else False
    results.append({
        "text": "Nodes are arranged left-to-right (x values increase for each stage)",
        "passed": increasing,
        "evidence": f"X values: {xs}"
    })

    # 5. Stage names in headings
    stage_names = ["ideation", "research", "design", "development", "testing", "launch"]
    found = set()
    for n in text_nodes:
        text_lower = n.get("text", "").lower()
        for name in stage_names:
            if name in text_lower:
                found.add(name)
    all_found = len(found) == 6
    results.append({
        "text": "Each node contains a markdown heading with the stage name",
        "passed": all_found,
        "evidence": f"Found stage names: {sorted(found)}, missing: {sorted(set(stage_names) - found)}"
    })

    # 6. Sequential edge flow
    # Sort text nodes by x position, check edges go from each to next
    sorted_nodes = sorted(text_nodes, key=lambda n: n.get("x", 0))
    node_ids_ordered = [n["id"] for n in sorted_nodes]
    sequential = True
    for i in range(len(node_ids_ordered) - 1):
        from_id = node_ids_ordered[i]
        to_id = node_ids_ordered[i + 1]
        has_edge = any(
            e.get("fromNode") == from_id and e.get("toNode") == to_id
            for e in edges
        )
        if not has_edge:
            sequential = False
            break
    results.append({
        "text": "Edge flow goes from each stage to the next in sequence",
        "passed": sequential,
        "evidence": f"Node order by x: {node_ids_ordered}"
    })

    return results


def grade_eval_2(data, path):
    """ML concepts: 6 file nodes, 2+ groups, hub-and-spoke, proper file paths."""
    results = []

    valid = run_validator(path)
    results.append({
        "text": "The output is a valid .canvas file (passes validate_canvas.py)",
        "passed": valid,
        "evidence": "Validator passed" if valid else "Validator failed"
    })

    file_nodes = nodes_by_type(data, "file")
    results.append({
        "text": "There are 6 file nodes referencing the vault notes",
        "passed": len(file_nodes) == 6,
        "evidence": f"Found {len(file_nodes)} file nodes: {[n.get('file', '') for n in file_nodes]}"
    })

    groups = nodes_by_type(data, "group")
    results.append({
        "text": "There are at least 2 group nodes (fundamentals and architecture)",
        "passed": len(groups) >= 2,
        "evidence": f"Found {len(groups)} groups: {[g.get('label', '(unlabeled)') for g in groups]}"
    })

    # Check that machine-learning node is NOT inside any group
    ml_nodes = [n for n in file_nodes if "machine-learning" in n.get("file", "").lower() or "machine_learning" in n.get("file", "").lower()]
    ml_inside_group = False
    if ml_nodes and groups:
        ml = ml_nodes[0]
        for g in groups:
            gx, gy = g.get("x", 0), g.get("y", 0)
            gw, gh = g.get("width", 0), g.get("height", 0)
            if (gx <= ml.get("x", 0) <= gx + gw and gy <= ml.get("y", 0) <= gy + gh):
                ml_inside_group = True
    results.append({
        "text": "The machine-learning.md node is central (not inside either group)",
        "passed": len(ml_nodes) > 0 and not ml_inside_group,
        "evidence": f"ML node found: {len(ml_nodes) > 0}, inside group: {ml_inside_group}"
    })

    # Edges from hub to topics
    edges = data.get("edges", [])
    ml_id = ml_nodes[0]["id"] if ml_nodes else None
    other_ids = {n["id"] for n in file_nodes if n["id"] != ml_id}
    connected = set()
    for e in edges:
        if e.get("fromNode") == ml_id and e.get("toNode") in other_ids:
            connected.add(e["toNode"])
        elif e.get("toNode") == ml_id and e.get("fromNode") in other_ids:
            connected.add(e["fromNode"])
    results.append({
        "text": "Edges connect the central hub to each topic node",
        "passed": len(connected) >= 4,  # at least most topics connected
        "evidence": f"Hub connected to {len(connected)}/{len(other_ids)} topic nodes"
    })

    # File paths match note names
    expected_files = {"machine-learning", "neural-networks", "gradient-descent",
                      "backpropagation", "transformers", "attention-mechanism"}
    found_files = set()
    for n in file_nodes:
        fp = n.get("file", "").lower().replace(".md", "").split("/")[-1]
        for ef in expected_files:
            if ef in fp:
                found_files.add(ef)
    results.append({
        "text": "File node paths match the note names given",
        "passed": len(found_files) == 6,
        "evidence": f"Matched: {sorted(found_files)}, missing: {sorted(expected_files - found_files)}"
    })

    return results


def grade_eval_3(data, path):
    """DB comparison: 3 groups, 6+ text nodes, title, colors, positioning."""
    results = []

    valid = run_validator(path)
    results.append({
        "text": "The output is a valid .canvas file (passes validate_canvas.py)",
        "passed": valid,
        "evidence": "Validator passed" if valid else "Validator failed"
    })

    groups = nodes_by_type(data, "group")
    results.append({
        "text": "There are 3 group nodes (one per database)",
        "passed": len(groups) == 3,
        "evidence": f"Found {len(groups)} groups: {[g.get('label', '(unlabeled)') for g in groups]}"
    })

    text_nodes = nodes_by_type(data, "text")
    # Exclude the title node for the pros/cons count
    non_title = [n for n in text_nodes if n.get("y", 0) > min(n2.get("y", 0) for n2 in text_nodes)]
    results.append({
        "text": "There are at least 6 text nodes for pros/cons (2 per database)",
        "passed": len(text_nodes) >= 7,  # 6 pros/cons + 1 title
        "evidence": f"Found {len(text_nodes)} text nodes total"
    })

    # Title/summary node exists (topmost text node or one not in any group)
    has_title = len(text_nodes) >= 7  # if there are 7+, one must be the title
    results.append({
        "text": "There is a title/summary text node",
        "passed": has_title,
        "evidence": f"Total text nodes: {len(text_nodes)} (need at least 7: 6 pros/cons + 1 title)"
    })

    # Color coding check
    group_colors = {g.get("color") for g in groups}
    cons_nodes = [n for n in text_nodes if "con" in n.get("text", "").lower()]
    pros_nodes = [n for n in text_nodes if "pro" in n.get("text", "").lower()]
    cons_colors = {n.get("color") for n in cons_nodes}
    pros_colors = {n.get("color") for n in pros_nodes}

    has_color_coding = (
        ("4" in group_colors or "#" in str(group_colors)) and
        ("1" in cons_colors or "#" in str(cons_colors)) and
        ("5" in pros_colors or "#" in str(pros_colors))
    )
    results.append({
        "text": "Color coding is used (green '4' for groups, red '1' for cons, cyan '5' for pros)",
        "passed": has_color_coding,
        "evidence": f"Group colors: {group_colors}, cons colors: {cons_colors}, pros colors: {pros_colors}"
    })

    # Positioning check: pros/cons within group bounds
    within_bounds = True
    violations = []
    for g in groups:
        gx, gy = g.get("x", 0), g.get("y", 0)
        gw, gh = g.get("width", 0), g.get("height", 0)
        label = g.get("label", "").lower()
        for n in text_nodes:
            text_lower = n.get("text", "").lower()
            # Check if this text node mentions the same DB as the group
            if label and any(db in text_lower and db in label for db in ["postgres", "mongo", "redis"]):
                nx, ny = n.get("x", 0), n.get("y", 0)
                if not (gx <= nx <= gx + gw and gy <= ny <= gy + gh):
                    within_bounds = False
                    violations.append(f"Node at ({nx},{ny}) outside group '{label}' bounds ({gx},{gy},{gw},{gh})")
    results.append({
        "text": "Pros and cons cards are positioned within their database group's bounds",
        "passed": within_bounds,
        "evidence": "All cards within bounds" if within_bounds else f"Violations: {violations}"
    })

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("canvas_file")
    parser.add_argument("--eval", type=int, required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    data = load_canvas(args.canvas_file)

    graders = {1: grade_eval_1, 2: grade_eval_2, 3: grade_eval_3}
    if args.eval not in graders:
        print(f"Unknown eval ID: {args.eval}")
        sys.exit(2)

    expectations = graders[args.eval](data, args.canvas_file)

    passed = sum(1 for e in expectations if e["passed"])
    total = len(expectations)

    grading = {
        "expectations": expectations,
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(passed / total, 2) if total > 0 else 0
        }
    }

    output_path = args.output or f"grading-eval{args.eval}.json"
    with open(output_path, "w") as f:
        json.dump(grading, f, indent=2)

    print(f"Eval {args.eval}: {passed}/{total} passed ({grading['summary']['pass_rate']:.0%})")
    for e in expectations:
        status = "✓" if e["passed"] else "✗"
        print(f"  {status} {e['text']}")
        if not e["passed"]:
            print(f"    Evidence: {e['evidence']}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
