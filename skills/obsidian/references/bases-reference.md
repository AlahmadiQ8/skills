# Obsidian Bases Reference

Bases are Obsidian's structured data views (`.base` files) — like spreadsheets or databases built on top of your notes. They pull data from note properties (frontmatter) and file metadata, display it in table/list/cards/map views, and support filters, formulas, sorting, and grouping. All data lives in your existing `.md` files — bases just provide structured views of it.

## Base File Format

A `.base` file is YAML with these sections:

```yaml
# Filters narrow results (default: all vault files)
filters:
  and:
    - file.inFolder("Projects")
    - file.ext == "md"

# Formulas create computed properties
formulas:
  tag_count: 'file.tags.length'
  status_label: 'if(file.hasTag("active"), "Active", "Inactive")'
  created_ago: 'file.ctime.relative()'

# Properties configure display names
properties:
  note.tags:
    displayName: "Tags"
  formula.status_label:
    displayName: "Status"

# Views define layouts
views:
  - type: table
    name: "All Projects"
    order:
      - file.name
      - formula.status_label
      - note.tags
      - note.date
      - file.mtime
  - type: table
    name: "Active Only"
    filters:
      and:
        - 'file.hasTag("active")'
    order:
      - file.name
      - note.tags
```

## View Types
- **table** — rows for files, columns for properties (most common)
- **list** — bulleted or numbered list
- **cards** — grid/gallery layout (great with images)
- **map** — pins on an interactive map (requires Maps plugin)

## Filter Syntax
Filters use `and`, `or`, `not` conjunctions with filter expressions:
```yaml
filters:
  or:
    - file.hasTag("book")
    - and:
        - file.inFolder("Reading")
        - 'status == "reading"'
    - not:
        - file.hasTag("archived")
```

## Key Filter/Formula Functions

### File functions
- `file.hasTag("tag")` — true if file has tag (includes nested tags)
- `file.inFolder("folder")` — true if file is in folder or subfolder
- `file.hasLink(otherFile)` — true if file links to another file
- `file.hasProperty("name")` — true if note has a property

### File properties
- `file.name`, `file.path`, `file.folder`, `file.ext`, `file.size`
- `file.ctime`, `file.mtime` — created/modified timestamps
- `file.tags` — all tags (inline + frontmatter)
- `file.links` — all internal links

### Note properties (frontmatter)
- Access via `note.property` or just `property` (shorthand)
- e.g., `note.status`, `status`, `note.tags`, `tags`

### Formula properties
- Access via `formula.name`
- e.g., `formula.tag_count`, `formula.status_label`

### Global functions
- `if(condition, trueResult, falseResult)` — conditional
- `now()` — current datetime; `today()` — current date
- `date("2026-01-01")` — parse date string
- `link("filename")` — create a link object
- `image(path)` — render image in view
- `min()`, `max()`, `number()`, `list()`

### Date functions
- `date.format("YYYY-MM-DD")` — format date
- `date.relative()` — "3 days ago" style output
- Date arithmetic: `now() - "7d"`, `date + "2w"`

### String/List functions
- `string.contains()`, `.lower()`, `.replace()`, `.split()`, `.title()`
- `list.filter(value > X)`, `.map(value + 1)`, `.sort()`, `.join(",")`, `.unique()`

## Embedding Bases in Notes

**Embed a .base file:**
```markdown
![](MyBase.base)
![](MyBase.base#ViewName)
```

**Inline base code block:**
````markdown
```base
filters:
  and:
    - file.hasTag("project")
views:
  - type: table
    name: "Projects"
    order:
      - file.name
      - note.tags
```
````

## CLI Bases Commands

**Important quirks discovered through testing:**
- `base:views` only works when the base is the **active file** — `file=` and `path=` parameters are ignored. Use `obsidian open path="MyBase.base"` first.
- `base:query` works with `file=` or `path=` targeting (doesn't need the base to be active).
- `file=` for bases requires the `.base` extension: `file="MyBase.base"`, not `file="MyBase"`.
- `base:create` with `path=` works and automatically places new files in the folder matching the base's filter.
- When using `base:create` with `content=`, frontmatter in the content string may not be parsed correctly. Instead, create the note first, then use `property:set` to add properties.

```bash
# List all .base files
obsidian bases

# List views (base must be active file)
obsidian open path="Projects.base" && sleep 1 && obsidian base:views

# Query a base (works with file=/path= targeting)
obsidian base:query file="Projects.base" format=json
obsidian base:query path="Projects.base" format=csv
obsidian base:query path="Projects.base" view="Active Only" format=json
obsidian base:query path="Projects.base" format=paths   # Just file paths
obsidian base:query path="Projects.base" format=md      # Markdown table
obsidian base:query path="Projects.base" format=tsv     # Tab-separated

# Create item in a base (respects base filter for file placement)
obsidian base:create path="Projects.base" name="New Project" content="# New Project"
# Then set properties separately:
obsidian property:set name=tags value="project, active" type=list file="New Project"
```

## Creating a Base from Scratch

To create a useful base programmatically:

1. **Create the `.base` file** with YAML defining filters, formulas, and views
2. **Ensure target notes have properties** — bases display frontmatter properties as columns
3. **Test with `base:query`** to verify filters and formulas work

Example — a task tracker base:
```yaml
filters:
  and:
    - file.hasTag("task")
formulas:
  overdue: 'if(due < today() && status != "done", "Overdue", "")'
  days_left: 'if(due, due.relative(), "")'
properties:
  note.status:
    displayName: "Status"
  note.due:
    displayName: "Due Date"
  formula.overdue:
    displayName: "Alert"
views:
  - type: table
    name: "All Tasks"
    order:
      - file.name
      - note.status
      - note.due
      - formula.overdue
      - formula.days_left
  - type: table
    name: "Overdue"
    filters:
      and:
        - 'formula.overdue == "Overdue"'
    order:
      - file.name
      - note.due
```

## Summaries

The `summaries` section defines aggregation formulas. Default summaries include: Average, Min, Max, Sum, Range, Median, Stddev, Earliest, Latest, Checked, Unchecked, Empty, Filled, Unique.

Custom summary example:
```yaml
summaries:
  customAverage: 'values.mean().round(3)'
```

In the view config, assign summaries to properties:
```yaml
views:
  - type: table
    name: "My Table"
    summaries:
      formula.price: Average
      note.score: Sum
```

## Operators Reference

### Arithmetic
`+`, `-`, `*`, `/`, `%`, `()`

### Comparison
`==`, `!=`, `>`, `<`, `>=`, `<=`

### Boolean
`!` (not), `&&` (and), `||` (or)

### Date Arithmetic
- Duration units: `y`/`year`, `M`/`month`, `d`/`day`, `w`/`week`, `h`/`hour`, `m`/`minute`, `s`/`second`
- Examples: `now() + "1d"`, `date - "2h"`, `file.mtime > now() - "1 week"`
- Subtract two dates to get milliseconds: `now() - file.ctime`
