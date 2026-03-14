# JavaScript API Reference

> **Sources:**
> - [JS API Intro](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/intro.md)
> - [Code Reference](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-reference.md)
> - [Data Array](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/data-array.md)
> - [Code Examples](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/api/code-examples.md)

## Table of Contents

1. [Overview](#overview)
2. [Query Methods](#query-methods)
3. [Render Methods](#render-methods)
4. [Dataview Render Methods](#dataview-render-methods)
5. [Markdown Render Methods](#markdown-render-methods)
6. [Utility Methods](#utility-methods)
7. [File I/O](#file-io)
8. [Query Evaluation](#query-evaluation)
9. [Data Arrays](#data-arrays)
10. [Examples](#examples)

---

## Overview

DataviewJS gives full JavaScript access to the Dataview index. Create blocks with:

~~~
```dataviewjs
dv.pages("#books").where(b => b.rating >= 7)
```
~~~

The `dv` variable provides the entire API. **Inline DataviewJS** uses `` `$= expression` `` syntax.

**Plugin access** (from other plugins or console):
```js
app.plugins.plugins.dataview.api
```

---

## Query Methods

### `dv.current()`
Page info for the current file.

### `dv.pages(source)`
Returns a DataArray of page objects matching the source (same syntax as DQL FROM).
```js
dv.pages()                           // all pages
dv.pages("#books")                   // pages with tag
dv.pages('"folder"')                 // pages in folder (double-quoted inside string)
dv.pages("#yes or -#no")             // tag logic
dv.pages('"folder" or #tag')         // combined
```

**Important:** Folders need double-quotes inside the string: `dv.pages('"folder"')` not `dv.pages("folder")`.

### `dv.pagePaths(source)`
Like `dv.pages()` but returns just file paths.

### `dv.page(path)`
Get full page object for a specific path or link. Auto-resolves extensions.
```js
dv.page("Index")                     // => page object for /Index
dv.page("books/The Raisin.md")      // => specific file
```

---

## Render Methods

### `dv.el(element, text, [options])`
Render text in any HTML element. Options: `cls` (CSS classes), `attr` (attributes).
```js
dv.el("b", "Bold text");
dv.el("b", "Styled", { cls: "my-class", attr: { alt: "Nice" } });
```

### `dv.header(level, text)`
Render header (level 1-6).

### `dv.paragraph(text)` / `dv.span(text)`
Render text in paragraph (with padding) or span (no padding).

### `dv.execute(source)`
Execute a DQL query and embed result.
```js
dv.execute("LIST FROM #tag");
dv.execute("TABLE field1, field2 FROM #thing");
```

### `dv.executeJs(source)`
Execute a DataviewJS query string.

### `dv.view(path, input)` ⌛
Load and execute a JS file, passing `dv` and `input`. Async — use `await`.
```js
await dv.view("views/custom", { arg1: "value" });
```
Supports `view.js` + `view.css` in a folder. Paths from vault root. Cannot start with `.`.

---

## Dataview Render Methods

### `dv.list(elements)`
Render a bullet list.
```js
dv.list([1, 2, 3])
dv.list(dv.pages().file.name)
dv.list(dv.pages("#book").where(p => p.rating > 7))
```

### `dv.taskList(tasks, [groupByFile])`
Render interactive task list. Groups by file by default; pass `false` for flat list.
```js
dv.taskList(dv.pages("#project").file.tasks)
dv.taskList(dv.pages("#project").file.tasks.where(t => !t.completed))
dv.taskList(dv.pages("#project").file.tasks, false)  // no grouping
```

### `dv.table(headers, elements)`
Render a table. `headers` = column names, `elements` = array of row arrays.
```js
dv.table(["File", "Genre", "Rating"],
    dv.pages("#book")
        .sort(b => b.rating)
        .map(b => [b.file.link, b.genre, b.rating]))
```

---

## Markdown Render Methods

Return markdown strings instead of rendering directly.

### `dv.markdownTable(headers, values)` / `dv.markdownList(values)` / `dv.markdownTaskList(tasks)`
Same as render versions but return markdown text.
```js
const table = dv.markdownTable(["File", "Rating"],
    dv.pages("#book").map(b => [b.file.link, b.rating]));
dv.paragraph(table);
```

---

## Utility Methods

| Method | Description | Example |
|--------|-------------|---------|
| `dv.array(value)` | Convert to DataArray | `dv.array([1,2,3])` |
| `dv.isArray(value)` | Check if array | `dv.isArray([1,2])` → `true` |
| `dv.fileLink(path, [embed], [display])` | Create link | `dv.fileLink("Note", false, "My Note")` |
| `dv.sectionLink(path, section, ...)` | Link to heading | `dv.sectionLink("Index", "Books")` |
| `dv.blockLink(path, blockId, ...)` | Link to block | `dv.blockLink("Notes", "12gdhjg3")` |
| `dv.date(text)` | Parse date | `dv.date("2021-08-08")` |
| `dv.duration(text)` | Parse duration | `dv.duration("8 minutes")` |
| `dv.compare(a, b)` | Compare values | Returns -1, 0, or 1 |
| `dv.equal(a, b)` | Check equality | `dv.equal(1, 1)` → `true` |
| `dv.clone(value)` | Deep clone | `dv.clone({a: 1})` |
| `dv.parse(value)` | Parse string to type | `dv.parse("[[A]]")` → Link |

---

## File I/O

All async (use `await`), under `dv.io`:

### `dv.io.csv(path, [origin])` ⌛
Load CSV as array of objects.
```js
await dv.io.csv("data.csv")  // => [{col1: ..., col2: ...}, ...]
```

### `dv.io.load(path, [origin])` ⌛
Load file contents as string.
```js
await dv.io.load("File")  // => "# File\nContent..."
```

### `dv.io.normalize(path, [origin])`
Resolve relative path to absolute.

---

## Query Evaluation

### `dv.query(source, [file, settings])` ⌛
Execute DQL query, return structured result.
```js
await dv.query("LIST FROM #tag")
// => { successful: true, value: { type: "list", values: [...] } }

await dv.query('TABLE WITHOUT ID file.name, value FROM "path"')
// => { successful: true, value: { type: "table", headers: [...], values: [...] } }
```

### `dv.tryQuery(source, ...)` ⌛
Same as `dv.query` but throws on failure instead of returning error result.

### `dv.queryMarkdown(source, ...)` ⌛ / `dv.tryQueryMarkdown(...)` ⌛
Execute DQL and return rendered markdown.

### `dv.tryEvaluate(expression, [context])`
Evaluate DQL expression. Throws on error.
```js
dv.tryEvaluate("2 + 2")  // => 4
dv.tryEvaluate("x + 2", {x: 3})  // => 5
```

### `dv.evaluate(expression, [context])`
Same but returns Result object (`result.successful`, `result.value`/`result.error`).

---

## Data Arrays

DataArrays are enhanced JavaScript arrays returned by most Dataview API calls.

### Key Features
- Regular indexing: `array[0]`
- **Swizzling**: `array.field` maps every element to `field` — `dv.pages().file.name` gets all file names
- Immutable operations (return new arrays)

### Methods

| Method | Description |
|--------|-------------|
| `where(pred)` / `filter(pred)` | Filter elements |
| `map(fn)` | Transform elements |
| `flatMap(fn)` | Map then flatten |
| `sort(key, [dir])` | Sort by key (`"asc"` or `"desc"`) |
| `groupBy(key)` | Group into `{key, rows}` objects |
| `distinct([key])` | Unique elements |
| `limit(n)` | Take first N elements |
| `slice(start, end)` | Array slice |
| `concat(other)` | Concatenate arrays |
| `find(pred)` | First matching element |
| `indexOf(elem)` | Index of element |
| `includes(elem)` | Contains check |
| `join(sep)` | Join to string |
| `every(pred)` | All match? |
| `some(pred)` | Any match? |
| `none(pred)` | None match? |
| `first()` / `last()` | First/last element |
| `to(key)` | Map to key then flatten |
| `expand(key)` | Recursively expand (for trees like subtasks) |
| `forEach(fn)` | Run function on each |
| `sum()` / `avg()` / `min()` / `max()` | Aggregations |
| `array()` | Convert to plain JS array |

---

## Examples

### Grouped books by genre
```js
for (let group of dv.pages("#book").groupBy(p => p.genre)) {
    dv.header(3, group.key);
    dv.table(["Name", "Time Read", "Rating"],
        group.rows
            .sort(k => k.rating, 'desc')
            .map(k => [k.file.link, k["time-read"], k.rating]))
}
```

### Find all directly and indirectly linked pages
```js
let page = dv.current().file.path;
let pages = new Set();
let stack = [page];
while (stack.length > 0) {
    let elem = stack.pop();
    let meta = dv.page(elem);
    if (!meta) continue;
    for (let inlink of meta.file.inlinks.concat(meta.file.outlinks).array()) {
        if (pages.has(inlink.path)) continue;
        pages.add(inlink.path);
        stack.push(inlink.path);
    }
}
let data = dv.array(Array.from(pages)).map(p => dv.page(p));
```

### Uncompleted tasks from project pages
```js
dv.taskList(
    dv.pages("#project").file.tasks
        .where(t => !t.completed),
    false
)
```

### Table with inline calculations
```js
dv.table(["File", "Days Since Modified"],
    dv.pages('"Projects"')
        .sort(p => p.file.mtime, "desc")
        .map(p => [p.file.link,
            Math.round((Date.now() - p.file.mtime) / (1000 * 60 * 60 * 24))
        ]))
```
