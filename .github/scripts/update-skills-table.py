#!/usr/bin/env python3
"""Parse skills/*/SKILL.md frontmatter and update the Available Skills table in README.md."""

import os
from pathlib import Path
import re
import sys


def parse_frontmatter(filepath):
    """Extract name and description from YAML frontmatter in a SKILL.md file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match YAML frontmatter between --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None

    frontmatter = match.group(1)

    # Extract name
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    name = name_match.group(1).strip().strip("\"'") if name_match else None

    # Extract description — handles both single-line and multi-line YAML scalars
    # Single-line: description: some text
    # Multi-line block scalar: description: >  or description: |
    desc_match = re.search(
        r"^description:\s*([>|])\s*\n((?:[ \t]+.+\n?)*)", frontmatter, re.MULTILINE
    )
    if desc_match:
        # Multi-line block scalar (folded > or literal |)
        raw_lines = desc_match.group(2)
        description = " ".join(line.strip() for line in raw_lines.strip().splitlines())
    else:
        # Single-line value
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
        description = (
            desc_match.group(1).strip().strip("\"'") if desc_match else None
        )

    if name and description:
        return {"name": name, "description": description}
    return None


def build_table(skills):
    """Build a markdown table from a list of skill dicts."""
    lines = [
        "| Skill | Description |",
        "|-------|-------------|",
    ]
    for skill in sorted(skills, key=lambda s: s["name"]):
        lines.append(f"| **{skill['name']}** | {skill['description']} |")
    return "\n".join(lines)


def main():
    repo_root = str(Path(__file__).resolve().parent.parent.parent)
    skills_dir = os.path.join(repo_root, "skills")
    readme_path = os.path.join(repo_root, "README.md")

    # Collect skills
    skills = []
    if os.path.isdir(skills_dir):
        for entry in sorted(os.listdir(skills_dir)):
            skill_file = os.path.join(skills_dir, entry, "SKILL.md")
            if os.path.isfile(skill_file):
                parsed = parse_frontmatter(skill_file)
                if parsed:
                    skills.append(parsed)
                else:
                    print(f"Warning: Could not parse frontmatter in {skill_file}", file=sys.stderr)

    if not skills:
        print("No skills found. Skipping README update.", file=sys.stderr)
        sys.exit(0)

    # Build new table
    table = build_table(skills)

    # Read current README
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()

    # Replace content between markers
    start_marker = "<!-- SKILLS-TABLE:START - Do not remove or modify this section -->"
    end_marker = "<!-- SKILLS-TABLE:END -->"

    pattern = re.escape(start_marker) + r".*?" + re.escape(end_marker)
    replacement = f"{start_marker}\n{table}\n{end_marker}"

    new_readme, count = re.subn(pattern, replacement, readme, flags=re.DOTALL)

    if count == 0:
        print(
            f"Error: Could not find skills table markers in {readme_path}. "
            f"Ensure the README contains '{start_marker}' and '{end_marker}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Write updated README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"Updated README.md with {len(skills)} skills.")


if __name__ == "__main__":
    main()
