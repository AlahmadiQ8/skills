# Functions Reference

> **Source:** [Functions](https://github.com/blacksmithgu/obsidian-dataview/blob/master/docs/docs/reference/functions.md)

## Table of Contents

1. [How Functions Work](#how-functions-work)
2. [Constructors](#constructors)
3. [Numeric Operations](#numeric-operations)
4. [Contains Functions](#contains-functions)
5. [Objects, Arrays, and String Operations](#objects-arrays-and-string-operations)
6. [String Operations](#string-operations)
7. [Utility Functions](#utility-functions)

---

## How Functions Work

Functions are expressions that can be used in data commands (except FROM) or as additional information in query types. Format: `functionname(param1, param2)`

**Vectorization:** Most functions can be applied to lists — they'll be applied to each element and return a list of results:
```
lower("YES") = "yes"
lower(["YES", "NO"]) = ["yes", "no"]
```

---

## Constructors

### `object(key1, value1, ...)`
Creates an object. Keys and values alternate, keys must be strings.
```
object("a", 6) => {"a": 6}
object("a", 4, "c", "yes") => {"a": 4, "c": "yes"}
```

### `list(value1, value2, ...)` / `array(...)`
Creates a list.
```
list(1, 2, 3) => [1, 2, 3]
```

### `date(any)` / `date(text, format)`
Parses a date from string, date, or link. Returns null on failure.
```
date("2020-04-18") = <Date April 18, 2020>
date([[2021-04-16]]) = <page's file.day>
date("12/31/2022", "MM/dd/yyyy") => December 31, 2022
```

### `dur(any)`
Parses a duration.
```
dur("8 minutes, 4 seconds") = <8m 4s>
```

### `number(string)`
Extracts first number from string.
```
number("18 years") = 18
number("hmm") = null
```

### `string(any)`
Converts to string representation.
```
string(18) = "18"
string(dur(8 hours)) = "8 hours"
```

### `link(path, [display])`
Creates a link object.
```
link("Hello") => link to 'Hello'
link("Hello", "Goodbye") => link to 'Hello' displayed as 'Goodbye'
```

### `embed(link, [embed?])`
Converts link to embedded link (mainly for images).
```
embed(link("Hello.png")) => embedded image
```

### `elink(url, [display])`
Creates external URL link.
```
elink("www.google.com", "Google") => link displayed as "Google"
```

### `typeof(any)`
Returns type name as string.
```
typeof(8) => "number"
typeof("text") => "string"
typeof([1,2,3]) => "array"
typeof({a:1}) => "object"
typeof(date(2020-01-01)) => "date"
typeof(dur(8 min)) => "duration"
```

---

## Numeric Operations

| Function | Description | Example |
|----------|-------------|---------|
| `round(n, [digits])` | Round to digits (default: whole) | `round(16.555, 2) = 16.56` |
| `trunc(n)` | Truncate decimal | `trunc(12.937) = 12` |
| `floor(n)` | Round down | `floor(-93.3) = -94` |
| `ceil(n)` | Round up | `ceil(12.937) = 13` |
| `min(a, b, ..)` | Minimum value | `min(1, 2, 3) = 1` |
| `max(a, b, ..)` | Maximum value | `max(1, 2, 3) = 3` |
| `sum(array)` | Sum all values | `sum([1, 2, 3]) = 6` |
| `product(array)` | Multiply all values | `product([1,2,3]) = 6` |
| `average(array)` | Numeric average | `average([1, 2, 3]) = 2` |
| `reduce(array, op)` | Reduce with operator (`+`,`-`,`*`,`/`,`&`,`\|`) | `reduce([100,20,3], "-") = 77` |
| `minby(arr, fn)` | Min by function | `minby(file.tasks, (k) => k.due)` |
| `maxby(arr, fn)` | Max by function | `maxby(file.tasks, (k) => k.due)` |

Use `nonnull()` to remove null values before aggregation: `sum(nonnull([null, 1, 8])) = 9`

---

## Contains Functions

### `contains(obj|list|str, value)` — case-sensitive
- **Objects:** checks if key exists — `contains(file, "ctime") = true`
- **Lists:** checks if any element equals value — `contains(list(1,2,3), 3) = true`
- **Strings:** checks substring — `contains("hello", "lo") = true`

### `icontains(obj|list|str, value)` — case-insensitive
Same as `contains` but ignores case.

### `econtains(obj|list|str, value)` — exact match
- **Strings:** same as `contains`
- **Lists:** exact word match — `econtains(["words"], "word") = false`, `econtains(["words"], "words") = true`
- **Objects:** exact key match (not recursive)

### `containsword(list|str, value)` — exact word, case-insensitive
- **Strings:** `containsword("Hello there!", "hello") = true`
- **Lists:** returns list of booleans

---

## Objects, Arrays, and String Operations

### `extract(object, key1, key2, ...)`
Pull specific fields from object.
```
extract(file, "ctime", "mtime") = object("ctime", file.ctime, "mtime", file.mtime)
```

### `sort(list)` / `reverse(list)`
```
sort(list(3, 2, 1)) = [1, 2, 3]
reverse(list(1, 2, 3)) = [3, 2, 1]
```

### `length(object|array)`
```
length([1, 2, 3]) = 3
length(object("a", 1, "b", 2)) = 2
```

### `nonnull(array)`
Remove null values: `nonnull([null, false]) = [false]`

### `firstvalue(array)`
First non-null value: `firstvalue([null, 1, 2]) => 1`

### `all(array, [fn])` / `any(array, [fn])` / `none(array, [fn])`
```
all([1, 2, 3], (x) => x > 0) = true
any([1, 2, 3], (x) => x > 2) = true
none([1, 2, 3], (x) => x = 0) = true
```

### `join(array, [delimiter])`
```
join(list(1, 2, 3)) = "1, 2, 3"
join(list(1, 2, 3), " ") = "1 2 3"
```

### `filter(array, predicate)`
```
filter([1, 2, 3], (x) => x >= 2) = [2, 3]
```

### `unique(array)`
```
unique([1, 3, 7, 3, 1]) => [1, 3, 7]
```

### `map(array, func)`
```
map([1, 2, 3], (x) => x + 2) = [3, 4, 5]
```

### `flat(array, [depth])`
Flatten nested arrays (default depth 1):
```
flat(list(1, 2, list(4, 5), 6)) => [1, 2, 4, 5, 6]
flat(rows.file.outlinks) => all outlinks flattened
```

### `slice(array, [start, [end]])`
```
slice([1,2,3,4,5], 3) = [4, 5]
slice(["a","b","c","d"], 0, 2) = ["a", "b"]
slice([1,2,3,4,5], -2) = [4, 5]
```

---

## String Operations

| Function | Description | Example |
|----------|-------------|---------|
| `regextest(pat, str)` | Regex found in string | `regextest("\\w+", "hello") = true` |
| `regexmatch(pat, str)` | Regex matches entire string | `regexmatch("what", "what's up?") = false` |
| `regexreplace(str, pat, repl)` | Regex replace all | `regexreplace("yes", "[ys]", "a") = "aea"` |
| `replace(str, pat, repl)` | String replace all | `replace("big dog", "big", "small")` |
| `lower(str)` / `upper(str)` | Case conversion | `lower("TEST") = "test"` |
| `split(str, delim, [limit])` | Split string (delimiter is regex) | `split("a b c", " ") = ["a","b","c"]` |
| `startswith(str, prefix)` | Check prefix | `startswith("path/to", "path/") = true` |
| `endswith(str, suffix)` | Check suffix | `endswith("hello.md", ".md") = true` |
| `padleft(str, len, [pad])` | Left-pad | `padleft("hi", 5, "!") = "!!!hi"` |
| `padright(str, len, [pad])` | Right-pad | `padright("hi", 5) = "hi   "` |
| `substring(str, start, [end])` | Extract substring | `substring("hello", 0, 2) = "he"` |
| `truncate(str, len, [suffix])` | Truncate with suffix | `truncate("Hello there!", 8) = "Hello..."` |

---

## Utility Functions

### `default(field, value)`
Returns `value` if `field` is null, else returns `field`.
```
default(dateCompleted, "incomplete")
```
Vectorized by default: `default(list(1, 2, null), 3) = [1, 2, 3]`
Use `ldefault()` to avoid vectorization on lists.

### `display()`
Converts to display string, preserving display properties of links/urls.
```
display(link("path/file.md")) = "file"
display(link("path/file.md", "custom")) = "custom"
```

### `choice(bool, left, right)`
If/else expression:
```
choice(true, "yes", "no") = "yes"
choice(x > 4, y, z) = y if x > 4, else z
```

### `hash(seed, [text], [variant])`
Generates a fixed hash for randomized sorting:
```
SORT hash(dateformat(date(today), "YYYY-MM-DD"), file.name)
```

### `striptime(date)`
Remove time component: `striptime(file.ctime) = file.cday`

### `dateformat(date, string)`
Format date using [Luxon tokens](https://moment.github.io/luxon/#/formatting?id=table-of-tokens):
```
dateformat(file.ctime, "yyyy-MM-dd") = "2022-01-05"
dateformat(file.ctime, "HH:mm:ss") = "12:18:04"
dateformat(date(now), "x") = "1407287224054"
```
Returns a **string**, not a date — can't compare against `date()` directly.

### `durationformat(duration, string)`
Format duration with tokens: `S` (ms), `s` (sec), `m` (min), `h` (hrs), `d` (days), `w` (weeks), `M` (months), `y` (years). Single-quoted text is literal.
```
durationformat(dur("3 days 7 hours 43 seconds"), "ddd'd' hh'h' ss's'") = "003d 07h 43s"
```

### `currencyformat(number, [currency])`
Format number as currency using ISO 4217 code:
```
currencyformat(123456.789, "EUR") = €123,456.79 (en_US locale)
```

### `localtime(date)`
Converts fixed-timezone date to current timezone.

### `meta(link)`
Access link metadata (not the linked page's data):
- `meta(link).display` — display text or null
- `meta(link).embed` — true if embed link (`![[...]]`)
- `meta(link).path` — path portion
- `meta(link).subpath` — heading text or block ID or null
- `meta(link).type` — `"file"`, `"header"`, or `"block"`

**Select tasks under a heading:**
~~~
```dataview
TASK
WHERE meta(section).subpath = "Next Actions"
```
~~~
