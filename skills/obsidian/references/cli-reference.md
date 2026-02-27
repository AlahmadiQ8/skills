# Obsidian CLI Quick Reference

Complete command reference for the `obsidian` CLI. All commands require Obsidian to be running.

## Table of Contents

1. [General](#general)
2. [Files and Folders](#files-and-folders)
3. [Properties](#properties)
4. [Links](#links)
5. [Tags](#tags)
6. [Tasks](#tasks)
7. [Daily Notes](#daily-notes)
8. [Templates](#templates)
9. [Search](#search)
10. [Bases](#bases)
11. [Bookmarks](#bookmarks)
12. [Plugins](#plugins)
13. [Commands](#commands)
14. [Outline](#outline)
15. [Vault](#vault)
16. [Workspace](#workspace)
17. [Sync](#sync)
18. [Publish](#publish)
19. [File History](#file-history)
20. [Themes & Snippets](#themes--snippets)
21. [Developer](#developer)

## Parameter Conventions

- `file=<name>` — resolves like internal links (shortest unique filename match, no path/extension needed)
- `path=<path>` — exact path from vault root (e.g. `folder/note.md`)
- If neither given, most commands default to the **active file**
- `vault=<name>` — must be first param to target a specific vault
- Flags are boolean switches: just include the name (e.g. `open`, `overwrite`)
- `--copy` — append to any command to copy output to clipboard
- Multiline content: `\n` for newline, `\t` for tab
- Quote values with spaces: `content="Hello world"`

## General

| Command | Description | Key Parameters |
|---|---|---|
| `help` | Show all commands | `<command>` for specific help |
| `version` | Show Obsidian version | — |
| `reload` | Reload app window | — |
| `restart` | Restart app | — |

## Files and Folders

| Command | Description | Key Parameters |
|---|---|---|
| `file` | Show file info | `file=`, `path=` |
| `files` | List vault files | `folder=`, `ext=`, `total` |
| `folder` | Show folder info | `path=` (required), `info=files\|folders\|size` |
| `folders` | List vault folders | `folder=`, `total` |
| `open` | Open a file | `file=`, `path=`, `newtab` |
| `create` | Create/overwrite file | `name=`, `path=`, `content=`, `template=`, `overwrite`, `open`, `newtab` |
| `read` | Read file contents | `file=`, `path=` |
| `append` | Append to file | `content=` (required), `file=`, `path=`, `inline` |
| `prepend` | Prepend after frontmatter | `content=` (required), `file=`, `path=`, `inline` |
| `move` | Move/rename file | `to=` (required), `file=`, `path=` |
| `rename` | Rename file | `name=` (required), `file=`, `path=` |
| `delete` | Delete file | `file=`, `path=`, `permanent` |

## Properties

| Command | Description | Key Parameters |
|---|---|---|
| `properties` | List properties | `file=`, `path=`, `name=`, `sort=count`, `format=yaml\|json\|tsv`, `total`, `counts`, `active` |
| `property:set` | Set property on file | `name=` (required), `value=` (required), `type=text\|list\|number\|checkbox\|date\|datetime`, `file=`, `path=` |
| `property:remove` | Remove property | `name=` (required), `file=`, `path=` |
| `property:read` | Read property value | `name=` (required), `file=`, `path=` |
| `aliases` | List aliases | `file=`, `path=`, `total`, `verbose`, `active` |

## Links

| Command | Description | Key Parameters |
|---|---|---|
| `backlinks` | List backlinks to file | `file=`, `path=`, `counts`, `total`, `format=json\|tsv\|csv` |
| `links` | List outgoing links | `file=`, `path=`, `total` |
| `unresolved` | List unresolved links | `total`, `counts`, `verbose`, `format=json\|tsv\|csv` |
| `orphans` | Files with no incoming links | `total` |
| `deadends` | Files with no outgoing links | `total` |

## Tags

| Command | Description | Key Parameters |
|---|---|---|
| `tags` | List tags | `file=`, `path=`, `sort=count`, `total`, `counts`, `format=json\|tsv\|csv`, `active` |
| `tag` | Get tag info | `name=` (required), `total`, `verbose` |

## Tasks

| Command | Description | Key Parameters |
|---|---|---|
| `tasks` | List tasks | `file=`, `path=`, `status="<char>"`, `total`, `done`, `todo`, `verbose`, `format=json\|tsv\|csv`, `active`, `daily` |
| `task` | Show/update task | `ref=<path:line>`, `file=`, `line=`, `status="<char>"`, `toggle`, `daily`, `done`, `todo` |

## Daily Notes

| Command | Description | Key Parameters |
|---|---|---|
| `daily` | Open daily note | `paneType=tab\|split\|window` |
| `daily:path` | Get daily note path | — |
| `daily:read` | Read daily note | — |
| `daily:append` | Append to daily note | `content=` (required), `inline`, `open` |
| `daily:prepend` | Prepend to daily note | `content=` (required), `inline`, `open` |

## Templates

| Command | Description | Key Parameters |
|---|---|---|
| `templates` | List templates | `total` |
| `template:read` | Read template | `name=` (required), `title=`, `resolve` |
| `template:insert` | Insert into active file | `name=` (required) |

## Search

| Command | Description | Key Parameters |
|---|---|---|
| `search` | Search vault | `query=` (required), `path=`, `limit=`, `format=text\|json`, `total`, `case` |
| `search:context` | Search with line context | `query=` (required), `path=`, `limit=`, `format=text\|json`, `case` |
| `search:open` | Open search view | `query=` |

## Bases

**Important:** `base:views` only works when the base is the active file — it ignores `file=`/`path=` params. `base:query` and `base:create` accept `file=`/`path=` targeting. The `file=` param for bases requires the `.base` extension (e.g., `file="Tasks.base"`, not `file="Tasks"`).

| Command | Description | Key Parameters |
|---|---|---|
| `bases` | List .base files | — |
| `base:views` | List views in base (**active file only**) | — |
| `base:create` | Create item in base | `file=`, `path=`, `view=`, `name=`, `content=`, `open`, `newtab` |
| `base:query` | Query base | `file=`, `path=`, `view=`, `format=json\|csv\|tsv\|md\|paths` |

## Bookmarks

| Command | Description | Key Parameters |
|---|---|---|
| `bookmarks` | List bookmarks | `total`, `verbose`, `format=json\|tsv\|csv` |
| `bookmark` | Add bookmark | `file=`, `subpath=`, `folder=`, `search=`, `url=`, `title=` |

## Plugins

| Command | Description | Key Parameters |
|---|---|---|
| `plugins` | List installed | `filter=core\|community`, `versions`, `format=json\|tsv\|csv` |
| `plugins:enabled` | List enabled | Same as `plugins` |
| `plugins:restrict` | Toggle restricted mode | `on`, `off` |
| `plugin` | Get plugin info | `id=` (required) |
| `plugin:enable` | Enable plugin | `id=` (required), `filter=core\|community` |
| `plugin:disable` | Disable plugin | `id=` (required), `filter=core\|community` |
| `plugin:install` | Install community plugin | `id=` (required), `enable` |
| `plugin:uninstall` | Uninstall plugin | `id=` (required) |
| `plugin:reload` | Reload plugin (dev) | `id=` (required) |

## Commands

| Command | Description | Key Parameters |
|---|---|---|
| `commands` | List command IDs | `filter=<prefix>` |
| `command` | Execute command | `id=` (required) |
| `hotkeys` | List hotkeys | `total`, `verbose`, `format=json\|tsv\|csv` |
| `hotkey` | Get hotkey for command | `id=` (required), `verbose` |

## Outline

| Command | Description | Key Parameters |
|---|---|---|
| `outline` | Show heading structure | `file=`, `path=`, `format=tree\|md\|json`, `total` |

## Vault

| Command | Description | Key Parameters |
|---|---|---|
| `vault` | Show vault info | `info=name\|path\|files\|folders\|size` |
| `vaults` | List known vaults | `total`, `verbose` |
| `vault:open` | Switch vault (TUI) | `name=` (required) |

## Workspace

| Command | Description | Key Parameters |
|---|---|---|
| `workspace` | Show workspace tree | `ids` |
| `workspaces` | List saved workspaces | `total` |
| `workspace:save` | Save workspace | `name=` |
| `workspace:load` | Load workspace | `name=` (required) |
| `workspace:delete` | Delete workspace | `name=` (required) |
| `tabs` | List open tabs | `ids` |
| `tab:open` | Open new tab | `group=`, `file=`, `view=` |
| `recents` | Recent files | `total` |

## Sync

| Command | Description | Key Parameters |
|---|---|---|
| `sync` | Pause/resume sync | `on`, `off` |
| `sync:status` | Show sync status | — |
| `sync:history` | Version history | `file=`, `path=`, `total` |
| `sync:read` | Read sync version | `file=`, `path=`, `version=` (required) |
| `sync:restore` | Restore sync version | `file=`, `path=`, `version=` (required) |
| `sync:open` | Open sync history | `file=`, `path=` |
| `sync:deleted` | List deleted files | `total` |

## Publish

| Command | Description | Key Parameters |
|---|---|---|
| `publish:site` | Show site info | — |
| `publish:list` | List published files | `total` |
| `publish:status` | List publish changes | `total`, `new`, `changed`, `deleted` |
| `publish:add` | Publish file | `file=`, `path=`, `changed` |
| `publish:remove` | Unpublish file | `file=`, `path=` |
| `publish:open` | Open on published site | `file=`, `path=` |

## File History

| Command | Description | Key Parameters |
|---|---|---|
| `diff` | List/compare versions | `file=`, `path=`, `from=`, `to=`, `filter=local\|sync` |
| `history` | List local versions | `file=`, `path=` |
| `history:list` | All files with history | — |
| `history:read` | Read history version | `file=`, `path=`, `version=` |
| `history:restore` | Restore version | `file=`, `path=`, `version=` (required) |

## Themes & Snippets

| Command | Description | Key Parameters |
|---|---|---|
| `themes` | List themes | `versions` |
| `theme` | Active theme info | `name=` |
| `theme:set` | Set active theme | `name=` (required) |
| `theme:install` | Install theme | `name=` (required), `enable` |
| `theme:uninstall` | Uninstall theme | `name=` (required) |
| `snippets` | List CSS snippets | — |
| `snippets:enabled` | List enabled snippets | — |
| `snippet:enable` | Enable snippet | `name=` (required) |
| `snippet:disable` | Disable snippet | `name=` (required) |

## Developer

| Command | Description | Key Parameters |
|---|---|---|
| `devtools` | Toggle dev tools | — |
| `dev:debug` | Attach/detach debugger | `on`, `off` |
| `dev:cdp` | Run CDP command | `method=` (required), `params=` |
| `dev:errors` | Show JS errors | `clear` |
| `dev:screenshot` | Take screenshot | `path=` |
| `dev:console` | Show console messages | `limit=`, `level=log\|warn\|error\|info\|debug`, `clear` |
| `dev:css` | Inspect CSS | `selector=` (required), `prop=` |
| `dev:dom` | Query DOM | `selector=` (required), `attr=`, `css=`, `total`, `text`, `inner`, `all` |
| `dev:mobile` | Toggle mobile emulation | `on`, `off` |
| `eval` | Execute JavaScript | `code=` (required) |
| `wordcount` | Word/char count | `file=`, `path=`, `words`, `characters` |
| `random` | Open random note | `folder=`, `newtab` |
| `random:read` | Read random note | `folder=` |
| `unique` | Create unique note | `name=`, `content=`, `open` |
| `web` | Open URL in viewer | `url=` (required), `newtab` |
