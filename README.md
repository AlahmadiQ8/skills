# Skills

A repository of my vibe coded skills. 

## Available Skills

<!-- SKILLS-TABLE:START - Do not remove or modify this section -->
| Skill | Description |
|-------|-------------|
| **hugo** | Build, configure, and develop Hugo static sites and themes. Use when the user wants to create a new Hugo site, develop or customize a Hugo theme, write Hugo templates (layouts, partials, shortcodes), configure hugo.toml/yaml/json, work with Hugo's asset pipeline (images, CSS/Sass, JS bundling), manage content (pages, sections, taxonomies, menus), or deploy a Hugo site. Triggers on mentions of "Hugo", "hugo.toml", "static site generator", Hugo-related template syntax (Go templates, baseof, partials), or Hugo content workflows. |
| **k6-load-testing** | Creates and runs Grafana k6 load testing scripts for traffic simulation, performance testing, and stress testing. Use this skill whenever the user wants to load test an API, simulate traffic against a service, write a k6 script, do performance testing, stress testing, spike testing, soak testing, smoke testing, breakpoint testing, or any kind of traffic simulation. Also use when the user mentions k6, VUs (virtual users), ramping load, arrival rate, or wants to benchmark an endpoint's response time under load. Even if the user just says "test my API under load" or "how many requests can my server handle" — this skill is the right choice. |
| **obsidian** | Edit and manage Obsidian vaults — create, read, update, and delete notes, manage properties/frontmatter, handle links and backlinks, work with tags, tasks, daily notes, templates, bases, and more. Uses the Obsidian CLI for safe vault operations when available, with direct file editing as fallback. Use this skill whenever the user mentions Obsidian, vault, knowledge base notes with wikilinks, frontmatter/properties on markdown files, daily notes, or any task involving an Obsidian vault — even if they just say "my notes" or reference a folder that looks like a vault (has .obsidian/ directory). |
| **obsidian-dataview** | Write Obsidian Dataview queries (DQL, inline DQL, and DataviewJS) from natural language descriptions. Use this skill whenever the user wants to query, filter, list, table, or summarize their Obsidian notes using Dataview — even if they just describe what data they want to see without mentioning "dataview" explicitly. Trigger on phrases like "show me all notes tagged...", "list my tasks due...", "table of books by rating", "query my vault for...", "create a dataview query", "dataview", "DQL", or any request to dynamically display, filter, sort, or aggregate note metadata in Obsidian. |
| **revealjs-slides** | Generate reveal.js HTML slide presentations from topics, outlines, or content. Use when the user asks to create slides, presentations, decks, or talks. Triggers on: "create a presentation", "make slides about", "build a deck", "generate a talk", "slide deck for", or any request involving presentation creation. Supports code highlighting, fragments, speaker notes, math, markdown, and Mermaid.js diagrams (flowcharts, sequence, class, ER, mindmap, timeline, etc.). |
<!-- SKILLS-TABLE:END -->

## Installation

Install all skills:

```bash
npx skills add alahmadiq8/skills
```

Install a specific skill:

```bash
npx skills add alahmadiq8/skills --skill fabric-icons -a claude-code
npx skills add alahmadiq8/skills --skill hugo -a claude-code
npx skills add alahmadiq8/skills --skill revealjs-slides -a claude-code
```

List available skills without installing:

```bash
npx skills add alahmadiq8/skills --list
```

## Awesome Skills Resources

- [anthropics/skills](https://github.com/anthropics/skills) - Official Anthropic skills
- [microsoft/skills](https://github.com/microsoft/skills) - Microsoft skills
- [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) - Anthropic knowledge work plugins
- [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) - Official Claude plugins
- [anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins) - Anthropics Financial Plugins
- [dotnet/skills](https://github.com/dotnet/skills/)
- [microsoft/azure-skills](https://github.com/microsoft/azure-skills)
- [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills)
