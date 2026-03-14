# Expressions and Literals Reference

> **Sources:**
> - [Expressions](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/expressions.md)
> - [Literals](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/literals.md)

## Table of Contents

1. [Expression Types](#expression-types)
2. [Literals](#literals)
3. [Date Literals](#date-literals)
4. [Duration Literals](#duration-literals)

---

## Expression Types

Expressions are anything that yields a value: fields, literals, arithmetic, comparisons, function calls, lambdas.

### Fields as Expressions
Refer to a field by name: `duedate`, `file.name`

Fields with spaces/punctuation use sanitized names: `this is a field` → `this-is-a-field`, `Hello!` → `hello`

### Literals
Constant values:

| Literal | Description |
|---------|-------------|
| `0`, `1337`, `-200` | Numbers |
| `"text"` | Text/string |
| `true`, `false` | Booleans |
| `[[Science]]` | Link to file |
| `[[]]` | Link to current file |
| `[1, 2, 3]` | List |
| `[[1,2],[3,4]]` | Nested lists |
| `{ a: 1, b: 2 }` | Object |
| `date(2021-07-14)` | Date |
| `dur(2 days 4 hours)` | Duration |

### Arithmetic
`+` (add), `-` (subtract), `*` (multiply), `/` (divide), `%` (modulo)

~~~
```dataview
TABLE start, end, (end - start) - dur(8 h) AS "Overtime"
FROM #work
```
~~~

### Comparisons
`<`, `>`, `<=`, `>=`, `=`, `!=`

Returns boolean for use in WHERE:
~~~
```dataview
LIST FROM "Games" WHERE price > 10
```
~~~

**Caution with type comparisons:** `null <= date(today)` returns `true`. Use `typeof()` or existence checks:
~~~
```dataview
TASK WHERE typeof(due) = "date" AND due <= date(today)
```
~~~

### String Operations
- Concatenation: `a + b` → `"Hello" + " " + "World"` = `"Hello World"`
- Repetition: `a * num` → `"!" * 3` = `"!!!"`

### List/Object Indexing
- List: `list[0]` (0-indexed)
- Object: `object["key"]` or `object.key`
- Nested: `episode_metadata["previous"]` or `episode_metadata.previous`
- Keyword fields: `row["where"]` (for fields named like DQL keywords)

### Function Calls
`function(arg1, arg2, ...)` — e.g., `lower(file.name)`, `contains(tags, "project")`

### Lambdas
Anonymous functions for use with `map`, `filter`, `any`, `all`, etc.:

```
(x) => x.field
(x, y) => x + y
(x) => 2 * x
(value) => length(value) = 4
```

~~~
```dataview
FLATTEN all(map(file.tasks, (x) => x.completed)) AS "allCompleted"
WHERE !allCompleted
```
~~~

### Link Indexing
Index through a link to get values from the target page:

`[[Assignment Math]].duedate` — gets `duedate` from the "Assignment Math" page

If a field contains a link (e.g., `Class:: [[Math]]`), index into it with `Class.timetable` (NOT `[[Class]].timetable`, which would look up a page literally called "Class").

---

## Date Literals

| Literal | Description |
|---------|-------------|
| `date(2021-11-11)` | Specific date |
| `date(2021-09-20T20:17)` | Date with time |
| `date(today)` | Current date |
| `date(now)` | Current date and time |
| `date(tomorrow)` | Tomorrow's date |
| `date(yesterday)` | Yesterday's date |
| `date(sow)` | Start of current week |
| `date(eow)` | End of current week |
| `date(som)` | Start of current month |
| `date(eom)` | End of current month |
| `date(soy)` | Start of current year |
| `date(eoy)` | End of current year |

`date()` is also a function that parses text/links into dates.

---

## Duration Literals

Format: `dur(<time> <unit>)`. Supports combinations.

### Units

| Unit | Short forms | Long forms |
|------|------------|------------|
| Seconds | `s`, `sec`, `secs` | `second`, `seconds` |
| Minutes | `m`, `min`, `mins` | `minute`, `minutes` |
| Hours | `h`, `hr`, `hrs` | `hour`, `hours` |
| Days | `d` | `day`, `days` |
| Weeks | `w`, `wk`, `wks` | `week`, `weeks` |
| Months | `mo` | `month`, `months` |
| Years | `yr`, `yrs` | `year`, `years` |

### Combinations
```
dur(1 s, 2 m, 3 h)     = 3 hours, 2 minutes, 1 second
dur(1s 2m 3h)           = same
dur(1second 2min 3h)    = same
```
