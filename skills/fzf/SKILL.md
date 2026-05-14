---
name: fzf
description: Use this skill whenever the user wants to use, compose, debug, or explain fzf commands: fuzzy file selection, interactive command-line pickers, multi-select workflows, previews, key bindings, shell integration, filtering lists, fuzzy finding when the exact name is unknown and only hints are available, or replacing ad-hoc grep/find menus with fzf. This skill helps Claude choose safe fzf options, use fzf as a pre-ranking tool with fd or find, build robust pipelines, and explain tradeoffs for interactive fuzzy finding.
compatibility: Requires the fzf CLI to be installed for running commands; generated examples assume a POSIX-like shell unless the user specifies otherwise.
license: Apache-2.0
---

# fzf

Use `fzf` when the user needs an interactive fuzzy picker for files, commands, history, logs, structured lists, or any stream of text. Favor it when a human should choose from many possible items, especially when the exact name is unknown and only partial hints are available, rather than when a deterministic script should make the choice automatically. When the source list is large or file-oriented, use `fd` or `find` to produce candidates and `fzf` as the pre-ranking and selection layer.

## Start by clarifying the execution context

Before running an interactive `fzf` command yourself, decide whether interaction is actually possible and useful:

- If the user asks for a command snippet, provide a copy-pasteable command and explain the important options briefly.
- If the task needs a human selection in the current terminal, ask the user to run the command with `! <command>` when appropriate so the interactive UI attaches to their session.
- If the environment is non-interactive, use `fzf --filter='query'` only for deterministic filtering, or build the command without executing it.
- If paths may contain spaces or newlines, prefer NUL-delimited pipelines with `--read0 --print0` when the surrounding tools support them.

## Common command patterns

### Pick files

```bash
selected=$(find . -type f -not -path '*/.git/*' -print | fzf --prompt='File> ' --preview='sed -n "1,120p" {}')
```

Use this for simple repositories. For large repos, prefer faster file producers if available:

```bash
selected=$(git ls-files | fzf --prompt='Tracked file> ' --preview='sed -n "1,120p" {}')
```

If filenames may contain unusual characters and downstream tooling supports NUL input:

```bash
find . -type f -print0 | fzf --read0 --print0 --prompt='File> '
```

### Pick multiple items

```bash
printf '%s\n' "$items" | fzf --multi --prompt='Select> '
```

Use `--multi=MAX` when the workflow expects a bounded number of selections.

### Filter without opening the UI

```bash
printf '%s\n' "$items" | fzf --filter='query'
```

Use `--filter` for scripts, tests, examples, or non-interactive environments. Add `--select-1 --exit-0` only when the intended behavior is clear: auto-accept one match and exit cleanly on no matches.

### Add previews

```bash
git ls-files | fzf \
  --prompt='File> ' \
  --preview='sed -n "1,160p" {}' \
  --preview-window='right:60%,wrap'
```

Keep previews read-only. Use tools such as `sed`, `bat`, `git diff --`, or `file` for inspection; avoid preview commands that mutate files or call network services.

### Work with columns or structured text

Use `--delimiter`, `--nth`, and `--with-nth` when only some fields should be searched or displayed:

```bash
ps -ef | fzf --header-lines=1 --delimiter=' +' --nth=8..
```

- `--nth` controls searchable fields.
- `--with-nth` controls displayed fields.
- `--accept-nth` controls printed fields on accept.
- Treat whitespace-parsed command output such as `ps` as platform-dependent; explain the column assumption or prefer a structured producer when correctness matters.

### Bind keys for common actions

```bash
git branch --all | fzf \
  --prompt='Branch> ' \
  --preview='git log --oneline --decorate --graph --color=always --max-count=30 {1}' \
  --ansi \
  --bind='ctrl-r:reload(git branch --all)'
```

Use `--bind` when the picker benefits from refresh, toggles, or alternate accept actions. Keep bindings discoverable with `--header` when sharing commands with users.

## Option selection guide

- Search behavior: use `--exact` for literal substring-like matching; keep the default smart-case fuzzy matching for general navigation.
- Path-heavy lists: use `--scheme=path` to improve ranking for file paths.
- History or recency lists: use `--scheme=history` when the input order carries meaning.
- ANSI-colored input: include `--ansi` so colors render correctly and matching ignores escape codes.
- Large or streaming input: consider `--tail=NUM` to cap memory, `--sync` for multi-stage filtering, or `--disabled` with reload bindings for external search tools.
- Layout: use `--height`, `--layout=reverse`, or `--popup` for shell widgets; keep full-screen mode for complex previews.
- Directory traversal: use `--walker`, `--walker-root`, and `--walker-skip` only when relying on fzf's built-in walker instead of piping input.

## Safety and robustness

- Quote placeholders in preview/action commands when paths may contain shell metacharacters. Prefer commands that accept `--` before paths, such as `git diff -- {}` where applicable.
- Do not build destructive bindings such as delete, reset, kill, or deploy actions unless the user explicitly asks and the command includes confirmation or a preview of the action.
- For process-killing or file-deleting workflows, default to printing the selected target and ask the user before executing the destructive command.
- Preserve user shell differences. The current session may use Fish, but generated snippets should match the user's requested shell. If no shell is specified, POSIX-style snippets are usually easiest to adapt.

## Troubleshooting

- If fzf is not found, tell the user it needs to be installed and provide high-level install guidance rather than guessing their package manager.
- If the UI does not appear, the command may be running in a non-interactive environment; suggest running it directly in a terminal.
- If previews are blank or slow, simplify the preview command, limit output length, and verify the placeholder receives the expected field.
- If matching feels wrong for columns, check `--delimiter`, `--nth`, and whether the input has a header.
- If colors show as escape codes, add `--ansi`.

## Response style

When helping with fzf:

1. Give the command first when the user asks for a command.
2. Mention any assumptions about shell, input source, or interactivity.
3. Briefly explain the few options that matter for the user's task.
4. If execution would be interactive or destructive, do not run it silently; ask the user to run or confirm it.
