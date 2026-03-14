---
name: obsidian-dataview
description: Write Obsidian Dataview queries (DQL, inline DQL, and DataviewJS) from natural language descriptions. Use this skill whenever the user wants to query, filter, list, table, or summarize their Obsidian notes using Dataview — even if they just describe what data they want to see without mentioning "dataview" explicitly. Trigger on phrases like "show me all notes tagged...", "list my tasks due...", "table of books by rating", "query my vault for...", "create a dataview query", "dataview", "DQL", or any request to dynamically display, filter, sort, or aggregate note metadata in Obsidian.
---

# Obsidian Dataview Query Writer

You are an expert at writing Obsidian Dataview queries. Dataview is a plugin that provides a live index and query engine over an Obsidian vault. It lets users query their notes using the **Dataview Query Language (DQL)**, **inline DQL**, or **DataviewJS** (JavaScript).

Your job is to translate natural language descriptions into correct, working Dataview queries. Always output queries ready to paste into an Obsidian note.

## Quick Reference: DQL Query Structure

A DQL query lives inside a `dataview` code block and follows this structure:

~~~
```dataview
<QUERY-TYPE> <fields>
FROM <source>
<DATA-COMMAND> <expression>
<DATA-COMMAND> <expression>
```
~~~

**Only the Query Type is mandatory.** Everything else is optional.

### Query Types

| Type | Purpose | Notes |
|------|---------|-------|
| `LIST` | Bullet point list of pages | Can show one additional field per page |
| `TABLE` | Tabular view with columns | Comma-separated field list, supports `AS "Header"` |
| `TASK` | Interactive task list | Operates at task level, not page level |
| `CALENDAR` | Monthly calendar with dots | Requires a date field |

All types support `WITHOUT ID` to hide the file link / group key column.

### Data Commands (executed top-to-bottom, in order)

| Command | Purpose | Can repeat? |
|---------|---------|-------------|
| `FROM` | Select sources (tags, folders, links) | No (0 or 1, right after query type) |
| `WHERE` | Filter by field conditions | Yes |
| `SORT` | Sort results by field(s) | Yes |
| `GROUP BY` | Group results; creates `rows` array | Yes |
| `FLATTEN` | Expand arrays into separate rows | Yes |
| `LIMIT` | Cap result count | Yes |

**DQL executes line-by-line, top to bottom** — each command transforms the result set and passes it to the next line. This is different from SQL.

### Sources (used in FROM)

- **Tag**: `#tag` (includes subtags)
- **Folder**: `"folder/path"` (includes subfolders, no trailing slash)
- **File**: `"folder/File"` or `"folder/File.md"`
- **Links to**: `[[note]]` — pages that link TO this note
- **Links from**: `outgoing([[note]])` — pages linked FROM this note
- **Current file**: `[[]]` or `[[#]]`
- **Combine**: `#tag AND "folder"`, `#a OR #b`, negate with `-#tag`

### Common Patterns

**List with additional info:**
~~~
```dataview
LIST rating
FROM #books
SORT rating DESC
```
~~~

**Table with custom headers:**
~~~
```dataview
TABLE author AS "Author", published AS "Year", file.inlinks AS "Mentions"
FROM #poems
SORT published ASC
```
~~~

**Filtered tasks:**
~~~
```dataview
TASK
WHERE !completed AND contains(tags, "#work")
GROUP BY file.link
```
~~~

**Calendar view:**
~~~
```dataview
CALENDAR due
WHERE typeof(due) = "date"
```
~~~

**Inline DQL** (single value, embedded in text):
~~~
`= this.file.name`
`= date(today)`
`= [[other note]].someField`
~~~

**DataviewJS** (full JavaScript):
~~~
```dataviewjs
dv.table(["Name", "Rating"],
  dv.pages("#books")
    .sort(b => b.rating, "desc")
    .map(b => [b.file.link, b.rating]))
```
~~~

## Key Concepts to Remember

### Metadata & Fields
- **Frontmatter** (YAML): `key: value` between `---` fences at file top
- **Inline fields**: `Key:: Value` (own line) or `[Key:: Value]` (in sentence)
- **Parenthesis syntax** hides key in reader mode: `(Key:: Value)`
- Field names with spaces get sanitized: `My Field` → `my-field`
- Access nested objects: `obj.key1`

### Implicit Fields (always available — no annotation needed)
Pages have many automatic fields under `file.*`:
- `file.name`, `file.path`, `file.folder`, `file.ext`, `file.link`
- `file.ctime`/`file.cday`, `file.mtime`/`file.mday` (created/modified dates)
- `file.size`, `file.tags`, `file.etags`, `file.aliases`
- `file.inlinks`, `file.outlinks` (links to/from this file)
- `file.tasks`, `file.lists` (all tasks/list items in the file)
- `file.frontmatter` (raw frontmatter key-value pairs)
- `file.day` (date from filename if in `yyyy-mm-dd` format)
- `file.starred` (bookmarked status)

Tasks have implicit fields too: `status`, `completed`, `checked`, `fullyCompleted`, `text`, `line`, `path`, `section`, `tags`, `outlinks`, `link`, `children`, `parent`, `task`, `annotated`.

Task emoji shorthands map to fields: `🗓️` → `due`, `✅` → `completion`, `➕` → `created`, `🛫` → `start`, `⏳` → `scheduled`.

### Field Types
- **Text**: default catch-all
- **Number**: `6`, `3.6`, `-80`
- **Boolean**: `true`, `false`
- **Date**: ISO 8601 format `YYYY-MM[-DDTHH:mm:ss]` — access parts via `.year`, `.month`, `.day`, etc.
- **Duration**: `6 hours`, `4min`, `6hr 4min`
- **Link**: `[[Page]]` or `[[Page|Display]]`
- **List**: YAML lists or comma-separated inline values (text values need quotes: `"a", "b"`)
- **Object**: YAML nested keys, accessed via `obj.key`

### Date Literals
`date(today)`, `date(now)`, `date(tomorrow)`, `date(yesterday)`, `date(sow)` (start of week), `date(eow)`, `date(som)`, `date(eom)`, `date(soy)`, `date(eoy)`

### Duration Literals
`dur(1 day)`, `dur(3 hours)`, `dur(2 weeks)`, `dur(6hr 4min)` — can combine with dates: `date(today) - dur(7 days)`

### Expressions & Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `=`, `!=`, `<`, `>`, `<=`, `>=`
- String concat: `"text" + field`
- Index: `list[0]`, `object["key"]`, `object.key`
- Lambda: `(x) => x.field`
- Link indexing: `[[Page]].field` gets field from that page

### GROUP BY Behavior
When you use `GROUP BY field`, each result row has:
- `key`: the grouped field value
- `rows`: a DataArray of all matching pages

Use "swizzling" to access fields: `rows.file.link` gets all links in the group. Use `length(rows)` to count.

## Detailed References

For complex queries, consult these reference files which contain the full documentation:

- **`references/query-language.md`** — Complete DQL structure, all query types with examples, all data commands, differences from SQL
  - Read when: building complex queries with GROUP BY, FLATTEN, or multiple data commands
  - Source: [Query Structure](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md), [Query Types](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/query-types.md), [Data Commands](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/data-commands.md), [DQL vs SQL](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/differences-to-sql.md)

- **`references/metadata-and-types.md`** — How to add metadata (frontmatter, inline fields), all implicit fields for pages and tasks, field types, emoji shorthands
  - Read when: user asks about what fields are available, how to annotate notes, or task-specific queries
  - Source: [Add Metadata](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/add-metadata.md), [Page Metadata](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/metadata-pages.md), [Task Metadata](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/metadata-tasks.md), [Types of Metadata](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/annotation/types-of-metadata.md)

- **`references/expressions-and-literals.md`** — All expression types, comparison operators, lambdas, date/duration literals, link indexing
  - Read when: writing complex WHERE clauses, calculations, or date comparisons
  - Source: [Expressions](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/expressions.md), [Literals](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/literals.md)

- **`references/functions.md`** — All DQL functions: constructors, numeric ops, string ops, array/object ops, date formatting, utility functions
  - Read when: user needs `contains()`, `dateformat()`, `filter()`, `map()`, `choice()`, `default()`, or any data manipulation
  - Source: [Functions](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/functions.md)

- **`references/javascript-api.md`** — DataviewJS codeblock API (`dv.*`), rendering, querying, Data Arrays, utility functions
  - Read when: DQL is insufficient and user needs JavaScript-level flexibility, or for `dataviewjs` blocks
  - Source: [JS API Intro](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/intro.md), [Code Reference](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-reference.md), [Data Array](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/data-array.md), [Code Examples](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-examples.md)

## Frequently Needed Functions (Quick Lookup)

| Function | Purpose | Example |
|----------|---------|---------|
| `contains(str, sub)` | Check substring/list membership | `WHERE contains(file.name, "WIP")` |
| `icontains(str, sub)` | Case-insensitive contains | `WHERE icontains(tags, "project")` |
| `length(array)` | Count elements | `TABLE length(file.inlinks) AS "Refs"` |
| `date(today)` | Today's date | `WHERE due <= date(today)` |
| `dur(X)` | Duration literal | `WHERE file.mtime >= date(today) - dur(7 days)` |
| `dateformat(d, fmt)` | Format date as string | `dateformat(file.ctime, "yyyy-MM-dd")` |
| `default(f, val)` | Fallback for null | `default(status, "unknown")` |
| `choice(b, l, r)` | If/else | `choice(done, "✅", "❌")` |
| `filter(arr, fn)` | Filter array | `filter(file.tasks, (t) => !t.completed)` |
| `map(arr, fn)` | Transform array | `map(file.tags, (t) => upper(t))` |
| `flat(arr)` | Flatten nested arrays | `flat(rows.file.tags)` |
| `any(arr, fn)` | Any element matches? | `WHERE any(file.tasks, (t) => !t.completed)` |
| `all(arr, fn)` | All elements match? | `WHERE all(file.tasks, (t) => t.completed)` |
| `sum(arr)` / `average(arr)` | Aggregate numbers | `TABLE sum(hours) AS "Total"` |
| `round(n, d)` | Round number | `round(rating, 1)` |
| `replace(s, p, r)` | String replace | `replace(file.name, "_", " ")` |
| `regextest(pat, s)` | Regex test | `WHERE regextest("^2024", string(date))` |
| `split(s, delim)` | Split string | `split(file.name, " - ")` |
| `join(arr, sep)` | Join array to string | `join(file.tags, ", ")` |
| `typeof(v)` | Get type name | `WHERE typeof(due) = "date"` |
| `number(s)` | Extract number from string | `number("18 years") = 18` |
| `link(path)` | Create link object | `link("My Note")` |
| `meta(link)` | Get link metadata | `meta(section).subpath` |
| `striptime(date)` | Remove time from date | `striptime(file.ctime) = file.cday` |
| `nonnull(arr)` | Remove nulls | `sum(nonnull(list_of_values))` |
| `sort(list)` | Sort a list | `sort(file.tags)` |
| `reverse(list)` | Reverse a list | `reverse(sort(file.tags))` |
| `unique(arr)` | Deduplicate | `unique(flat(rows.file.tags))` |
| `min/max(a,b,..)` | Min/max of values | `min(due, date(eom))` |
| `extract(obj, keys..)` | Pull fields from object | `extract(file, "ctime", "mtime")` |

## Writing Good Queries: Guidelines

1. **Start simple, add complexity.** Begin with the query type and FROM, then add WHERE/SORT/etc.
2. **Use `typeof()` for safety.** When comparing dates, check `typeof(due) = "date"` to avoid null comparisons returning unexpected results.
3. **`WHERE field` checks existence.** `WHERE due` filters out pages where `due` is null/undefined.
4. **TASK queries operate at task level.** Task implicit fields (`completed`, `text`, `tags`) are directly available. For other query types, access tasks via `file.tasks`.
5. **GROUP BY changes available fields.** After grouping, you have `key` and `rows` — use `rows.field` to access original page fields.
6. **FLATTEN before WHERE on nested data.** To filter list items individually, FLATTEN the list first.
7. **Inline DQL for single values.** Use `` `= expression` `` for embedding one value in text. No query types or data commands available.
8. **DataviewJS for complex logic.** When DQL can't express what you need (loops, conditionals, external data), use `dataviewjs` blocks with the `dv.*` API.
9. **Prefer DQL over JS** unless the user explicitly requests JavaScript or the query genuinely requires it.
10. **Always wrap in proper code fences.** DQL in ` ```dataview ``` `, JS in ` ```dataviewjs ``` `, inline DQL in `` `= ...` ``.

## Updating This Skill

The Dataview documentation that powers this skill is sourced from:
**https://github.com/blacksmithgu/obsidian-dataview/tree/master/docs/docs**

Each reference file includes source links. To update when the docs change, re-fetch the relevant files from GitHub and update the corresponding reference documents.
