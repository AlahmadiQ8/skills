# Metadata and Types Reference

> **Sources:**
> - [Add Metadata](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/add-metadata.md)
> - [Metadata on Pages](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/metadata-pages.md)
> - [Metadata on Tasks and Lists](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/metadata-tasks.md)
> - [Types of Metadata](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/types-of-metadata.md)

## Table of Contents

1. [Adding Metadata](#adding-metadata)
2. [Field Names](#field-names)
3. [Implicit Fields on Pages](#implicit-fields-on-pages)
4. [Implicit Fields on Tasks and Lists](#implicit-fields-on-tasks-and-lists)
5. [Task Emoji Shorthands](#task-emoji-shorthands)
6. [Field Types](#field-types)

---

## Adding Metadata

### Frontmatter (YAML)

YAML at the top of the file between `---` fences. All frontmatter fields are automatically Dataview fields.

```yaml
---
alias: "document"
last-reviewed: 2021-08-17
thoughts:
  rating: 8
  reviewable: false
---
```

Query nested objects with dot notation: `thoughts.rating`

### Inline Fields

Use `Key:: Value` syntax anywhere in the file.

**Own line (field takes full line after `::`):**
```markdown
Basic Field:: Some random Value
**Bold Field**:: Nice!
```

**In-sentence (bracket syntax):**
```markdown
I would rate this a [rating:: 9]! It was [mood:: acceptable].
```

Bracketed inline fields are the **only** way to add fields to specific list items or tasks:
```markdown
- [ ] Send mail to David about deadline [due:: 2022-04-05].
```

**Parenthesis syntax** hides the key in Reader mode:
```markdown
This will not show the (longKeyIDontNeedWhenReading:: key).
```

You can mix YAML frontmatter and inline fields in the same file.

### Important: Only indexed data is queryable

Dataview cannot query arbitrary paragraph text. Only metadata fields (frontmatter, inline fields) and automatically-indexed content (tags, list items, tasks) are available.

---

## Field Names

- Fields with **spaces** get sanitized: `Basic Field` → `basic-field`
- Fields with **capitalized letters** can be used as-is or via sanitized lowercase version
- **Formatting tokens** (bold, italic, etc.) are stripped from key names
- **Emojis** can be used as keys but must be in `[brackets]`: `[🎅:: a console game]`
- UTF-8 characters are fully supported

Access fields with spaces:
1. Sanitized name: `field-with-space`
2. Row syntax: `row["Field With Space"]`

Access fields named like keywords (from, where, etc.):
- `row.from`, `row.where`, `row["where"]`

---

## Implicit Fields on Pages

These are automatically available on every page under the `file` namespace:

| Field | Type | Description |
|-------|------|-------------|
| `file.name` | Text | Filename as shown in sidebar |
| `file.folder` | Text | Path of containing folder |
| `file.path` | Text | Full file path including name |
| `file.ext` | Text | File extension (usually `md`) |
| `file.link` | Link | A link to the file |
| `file.size` | Number | File size in bytes |
| `file.ctime` | Date+Time | Creation date and time |
| `file.cday` | Date | Creation date (no time) |
| `file.mtime` | Date+Time | Last modified date and time |
| `file.mday` | Date | Last modified date (no time) |
| `file.tags` | List | All unique tags (subtags broken down: `#Tag/1/A` → `[#Tag, #Tag/1, #Tag/1/A]`) |
| `file.etags` | List | Explicit tags only (not broken down) |
| `file.inlinks` | List | All incoming links (files that link to this file) |
| `file.outlinks` | List | All outgoing links (links in this file) |
| `file.aliases` | List | Aliases from YAML frontmatter |
| `file.tasks` | List | All tasks (`- [ ] ...`) in the file |
| `file.lists` | List | All list items (including tasks) |
| `file.frontmatter` | List | Raw frontmatter as `key | value` pairs |
| `file.day` | Date | Date from filename (if `yyyy-mm-dd` or `yyyymmdd` format) or from a `Date` field |
| `file.starred` | Boolean | Whether bookmarked via core Bookmarks plugin |

---

## Implicit Fields on Tasks and Lists

Tasks inherit **all fields** from their parent page — if the page has `rating`, you can access it on tasks too.

| Field | Type | Description |
|-------|------|-------------|
| `status` | Text | Character inside `[ ]` brackets (space for incomplete, `x` for complete) |
| `checked` | Boolean | True if status is NOT empty (has some character in brackets) |
| `completed` | Boolean | True if specifically marked `[x]` |
| `fullyCompleted` | Boolean | True if this task AND all subtasks are completed |
| `text` | Text | Plain text of the task, including metadata annotations |
| `visual` | Text | Rendered text (can be overridden in DataviewJS) |
| `line` | Number | Line number in file |
| `lineCount` | Number | Number of markdown lines the task spans |
| `path` | Text | Full path of containing file |
| `section` | Link | Link to the section containing this task |
| `tags` | List | Tags inside the task text |
| `outlinks` | List | Links defined in this task |
| `link` | Link | Link to nearest linkable block |
| `children` | List | Subtasks or sublists of this task |
| `task` | Boolean | True if this is a task; false for regular list items |
| `annotated` | Boolean | True if task text contains metadata fields |
| `parent` | Number | Line number of parent task (null if root-level) |
| `blockId` | Text | Block ID if defined with `^blockId` syntax |

### Accessing in queries

In **TASK** queries, task fields are directly available:
~~~
```dataview
TASK
WHERE !fullyCompleted
```
~~~

In other query types, access via `file.lists` or `file.tasks`:
~~~
```dataview
LIST
WHERE any(file.tasks, (t) => !t.fullyCompleted)
```
~~~

---

## Task Emoji Shorthands

The Tasks plugin emoji notation is supported. No `[key:: value]` syntax needed:

| Field Name | Shorthand | Example |
|-----------|-----------|---------|
| `due` | `🗓️YYYY-MM-DD` | `- [ ] Task 🗓️2021-08-29` |
| `completion` | `✅YYYY-MM-DD` | `- [x] Done ✅2021-08-22` |
| `created` | `➕YYYY-MM-DD` | `- [ ] New ➕1990-06-14` |
| `start` | `🛫YYYY-MM-DD` | `- [ ] Can start 🛫2021-08-29` |
| `scheduled` | `⏳YYYY-MM-DD` | `- [x] Scheduled ⏳2021-08-29` |

Query by textual field name:
~~~
```dataview
TASK
WHERE completion = date("2021-08-22")
```
~~~

Both shorthands and `[completion:: 2021-08-22]` are matched.

---

## Field Types

### Text
Default catch-all. If a field doesn't match a more specific type, it's text.
```markdown
Example:: This is some normal text.
```

Multiline text only possible via YAML `|` pipe operator.

### Number
```markdown
Example:: 6
Example:: 2.4
Example:: -80
```
In YAML, write without quotes: `rating: 8`

### Boolean
```markdown
Example:: true
Example:: false
```

### Date
ISO 8601 format: `YYYY-MM[-DDTHH:mm:ss.nnn+ZZ]`
```markdown
Example:: 2021-04
Example:: 2021-04-18
Example:: 2021-04-18T04:19:35.000
Example:: 2021-04-18T04:19:35.000+06:30
```

Access date parts: `.year`, `.month`, `.weekyear`, `.week`, `.weekday`, `.day`, `.hour`, `.minute`, `.second`, `.millisecond`

```
WHERE birthday.month = date(now).month
```

### Duration
`<time> <unit>` format. Common abbreviations accepted. Multiple units combinable.
```markdown
Example:: 7 hours
Example:: 16days
Example:: 4min
Example:: 6hr7min
Example:: 9 years, 8 months, 4 days, 16 hours, 2 minutes
```

Dates and durations are compatible — you can add/subtract them:
```
departure + length-of-travel = arrival date
release-date - date(now) = time until release
```

### Link
```markdown
Example:: [[A Page]]
Example:: [[Some Other Page|Render Text]]
```

In YAML frontmatter, links must be quoted: `parent: "[[parentPage]]"`. Note: quoted links are only Dataview links, not Obsidian links (won't show in graph view or outgoing links).

### List
YAML:
```yaml
key3: [one, two, three]
key4:
  - four
  - five
```

Inline (text values need quotes):
```markdown
Example1:: 1, 2, 3
Example2:: "yes", "or", "no"
```

Duplicate metadata keys in the same file automatically become a list.

### Object
YAML only:
```yaml
obj:
  key1: "Val"
  key2: 3
  key3:
    - "List1"
    - "List2"
```

Access: `obj.key1`, `obj.key2`, `obj.key3`
