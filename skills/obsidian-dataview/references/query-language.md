# Dataview Query Language Reference

> **Sources:**
> - [Query Structure](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/structure.md)
> - [Query Types](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/query-types.md)
> - [Data Commands](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/data-commands.md)
> - [DQL, JS and Inlines](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/dql-js-inline.md)
> - [Differences to SQL](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/queries/differences-to-sql.md)
> - [Sources](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/sources.md)
> - [Examples](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/resources/examples.md)
> - [FAQ](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/resources/faq.md)

## Table of Contents

1. [General Format](#general-format)
2. [Query Types](#query-types)
   - [LIST](#list)
   - [TABLE](#table)
   - [TASK](#task)
   - [CALENDAR](#calendar)
3. [Sources (FROM)](#sources)
4. [Data Commands](#data-commands)
5. [Inline DQL](#inline-dql)
6. [DQL vs SQL Differences](#dql-vs-sql-differences)
7. [Examples](#examples)
8. [FAQ](#faq)

---

## General Format

Every DQL query follows this pattern:

~~~
```dataview
<QUERY-TYPE> <fields>
FROM <source>
<DATA-COMMAND> <expression>
<DATA-COMMAND> <expression>
```
~~~

Only the Query Type is mandatory. Commands execute top-to-bottom, each transforming the result set.

---

## Query Types

### LIST

Outputs a bullet point list of file links. Can show one additional field per page.

~~~
```dataview
LIST
```
~~~

**With additional info:**
~~~
```dataview
LIST file.folder
FROM #games
```
~~~

Output: `- [League of Legends]: Games`

**Computed values:**
~~~
```dataview
LIST "File Path: " + file.folder + " _(created: " + file.cday + ")_"
FROM "Games"
```
~~~

**Grouped LIST:**
~~~
```dataview
LIST rows.file.link
GROUP BY type
```
~~~

Shows group keys with their pages nested underneath.

**LIST WITHOUT ID** — hides file link/group key:
~~~
```dataview
LIST WITHOUT ID length(rows) + " pages of type " + key
GROUP BY type
```
~~~

### TABLE

Outputs a table. Supports zero to many comma-separated columns with optional `AS "Header"` aliases.

~~~
```dataview
TABLE started, file.folder, file.etags
FROM #games
```
~~~

**Custom headers:**
~~~
```dataview
TABLE started, file.folder AS Path, file.etags AS "File Tags"
FROM #games
```
~~~

**Calculations as columns:**
~~~
```dataview
TABLE
  default(finished, date(today)) - started AS "Played for",
  file.folder AS Path
FROM #games
```
~~~

**TABLE WITHOUT ID** — removes the File/Group column:
~~~
```dataview
TABLE WITHOUT ID
  file.link AS "Game",
  file.etags AS "File Tags"
FROM #games
```
~~~

The first column always shows result count (disable in Dataview settings → "Display result count").

### TASK

Outputs an interactive task list. Operates at **task level** (not page level), so data commands filter individual tasks.

~~~
```dataview
TASK
WHERE !completed AND contains(tags, "#shopping")
```
~~~

**Group by file:**
~~~
```dataview
TASK
WHERE !completed
GROUP BY file.link
```
~~~

**Important: Child tasks** belong to their parent. If the parent matches a query, all children are included even if they don't individually match. If only a child matches but parent doesn't, only that child is returned.

**Task interaction:** Checking a task in a Dataview result also checks it in the original file.

### CALENDAR

Renders a monthly calendar with dots on dates. Requires one date field.

~~~
```dataview
CALENDAR file.ctime
```
~~~

**Filter for valid dates:**
~~~
```dataview
CALENDAR due
WHERE typeof(due) = "date"
```
~~~

SORT and GROUP BY have no effect on CALENDAR.

---

## Sources

Sources identify sets of files and are used in the FROM command.

### Tag Sources
`FROM #tag` — matches all files with the given tag (including subtags).

### Folder Sources
`FROM "folder"` — matches all files in the folder and subfolders. Use full vault path. No trailing slash.

### File Sources
`FROM "path/to/File"` — select a specific file. Add `.md` to disambiguate from a folder with the same name.

### Link Sources
- `FROM [[note]]` — all pages that link TO this note
- `FROM outgoing([[note]])` — all pages linked FROM this note
- `FROM [[]]` or `FROM [[#]]` — all pages linking to the current file

### Combining Sources
- `#tag AND "folder"` — both conditions
- `#food OR #exercise` — either condition
- `-#tag` — negate (exclude)
- `(#tag1 OR #tag2) AND (#tag3 OR #tag4)` — parentheses for grouping

---

## Data Commands

### FROM
Determines initial page set. Zero or one, must come right after query type.

### WHERE
Filters pages/tasks by condition. Only rows where clause is `true` pass through.

~~~
```dataview
LIST WHERE file.mtime >= date(today) - dur(1 day)
```
~~~

~~~
```dataview
LIST FROM #projects
WHERE !completed AND file.ctime <= date(today) - dur(1 month)
```
~~~

### SORT
Sorts results. Specify `ASC`/`ASCENDING` or `DESC`/`DESCENDING`. Multiple fields for tie-breaking:

~~~
```dataview
SORT field1 DESC, field2 ASC
```
~~~

### GROUP BY
Groups results. Each row gets a `key` (the group value) and `rows` (DataArray of pages in that group). Use "swizzling": `rows.field` gets that field from every page in the group.

~~~
```dataview
GROUP BY type
GROUP BY (computed_field) AS name
```
~~~

### FLATTEN
Expands an array field into separate rows (one per element):

~~~
```dataview
TABLE authors FROM #LiteratureNote
FLATTEN authors
```
~~~

Before FLATTEN: one row per file. After: one row per author.

Very useful for `file.lists`, `file.tasks`, or any multi-value field:
~~~
```dataview
TABLE T.text AS "Task Text"
FROM "Scratchpad"
FLATTEN file.tasks AS T
WHERE T.text
```
~~~

### LIMIT
Restrict result count:
~~~
```dataview
LIMIT 5
```
~~~

Commands execute in order, so `LIMIT 5` then `SORT date ASC` limits first, then sorts the limited set.

---

## Inline DQL

Inline queries display exactly one value embedded in text. Default prefix is `=`:

~~~
`= this.file.name`
`= date(today)`
`= this.someField`
`= [[otherPage]].field`
`= choice(this.steps > 10000, "YES!", "No, get moving!")`
~~~

Supports all expressions and functions, but NOT query types or data commands.

Change prefix in Dataview settings → "Codeblock Settings" → "Inline Query Prefix".

---

## DQL vs SQL Differences

- DQL executes **top to bottom, line by line** (like a pipeline, not a declarative query)
- Each line passes its full result set to the next line
- You can have **multiple WHERE**, **multiple SORT**, **multiple GROUP BY** — this is valid in DQL
- First line is Query Type (like SQL's SELECT determines output format)
- Second line (optional) is FROM (filters sources, similar to SQL's WHERE on table selection)
- Subsequent lines are data commands that reshape the running result set

---

## Examples

**All games sorted by rating:**
~~~
```dataview
TABLE time-played AS "Time Played", length AS "Length", rating AS "Rating"
FROM "games"
SORT rating DESC
```
~~~

**MOBAs or CRPGs:**
~~~
```dataview
LIST FROM #games/mobas OR #games/crpg
```
~~~

**Tasks from a project:**
~~~
```dataview
TASK FROM "dataview"
```
~~~

**Books by last modified:**
~~~
```dataview
TABLE file.mtime AS "Last Modified"
FROM "books"
SORT file.mtime DESC
```
~~~

**Files with dates in name:**
~~~
```dataview
LIST file.day WHERE file.day
SORT file.day DESC
```
~~~

**Recent files with a tag:**
~~~
```dataview
LIST
FROM #status/open
SORT file.ctime DESC
LIMIT 10
```
~~~

**Overdue tasks:**
~~~
```dataview
TASK
WHERE !completed AND typeof(due) = "date" AND due < date(today)
SORT due ASC
```
~~~

**Flatten and filter nested lists:**
~~~
```dataview
TABLE L.text AS "My lists"
FROM "dailys"
FLATTEN file.lists AS L
WHERE contains(L.author, "Surname")
```
~~~

---

## FAQ

### How do I use fields with the same name as keywords (like "from", "where")?
Use the special `row` field:
```
row.from
row.where
```

### How do I access fields with spaces?
1. Use the sanitized name: `Field With Space` → `field-with-space`
2. Use `row["Field With Space In It"]`

### Can I save a query result for reuse?
Use Inline DQL in a metadata field:
```markdown
duration:: `= this.end - this.start - this.pause`
```
The displayed value is calculated, but the stored value is the expression text — you can't filter on the computed result.

### How can I hide the result count?
Dataview settings → "Display result count" (available since 0.5.52).
