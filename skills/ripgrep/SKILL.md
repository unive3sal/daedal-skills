---
name: ripgrep
description: Use this skill whenever the user wants to search text in files, codebases, logs, books, or documents; find occurrences, definitions, references, TODOs, errors, literals, regex matches, or multiline patterns; replace slow grep commands; compose, debug, or explain rg/ripgrep commands; or search file contents before editing, reviewing, refactoring, or feeding matches into fzf, xargs, editors, or scripts. Prefer rg as the primary text-search tool because it is much faster than native grep, searches recursively by default, respects ignore files, skips hidden and binary files by default, and has ergonomic filters for file types, globs, context, JSON output, and replacements. If rg is unavailable, fall back to grep.
compatibility: Requires the rg CLI for preferred commands; if rg is not installed, fall back to grep. Generated examples assume a POSIX-like shell unless the user specifies otherwise.
license: Apache-2.0
---

# ripgrep

Use `rg` as the first-choice tool for searching text inside files. It is usually much faster than native `grep`, searches directories recursively by default, respects `.gitignore` and other ignore files, and skips hidden files, ignored files, and binary files unless asked otherwise. Fall back to `grep` when `rg` is not installed, when strict POSIX portability matters, or when a system script cannot depend on extra tools.

## Start with tool availability

Before running an `rg` command, check whether `rg` is available when the environment is uncertain:

```bash
command -v rg >/dev/null 2>&1
```

- If `rg` exists, use it for text search.
- If `rg` is missing, use `grep` and keep the fallback as close as practical to the intended `rg` behavior.
- If providing a reusable snippet, include a fallback only when useful; otherwise mention that `grep` is the fallback.

## Command shape

`rg` uses these common forms:

```bash
rg [OPTIONS] PATTERN [PATH ...]
rg [OPTIONS] -e PATTERN ... [PATH ...]
rg [OPTIONS] -f PATTERNFILE ... [PATH ...]
command | rg [OPTIONS] PATTERN
```

Important differences from `grep`:

- Directories are searched recursively by default.
- Patterns are regular expressions by default.
- Hidden files, ignored files, and binary files are skipped by default.
- File paths specified on the command line override glob and ignore rules.
- If a pattern starts with `-`, pass it with `-e` or use `--`: `rg -e '-foo'`.

## Common command patterns

### Search recursively

```bash
rg 'pattern' .
```

Fallback:

```bash
grep -R --line-number 'pattern' .
```

Use a narrower path whenever possible to reduce noise and speed up the search:

```bash
rg 'pattern' src tests
```

### Search literal text

```bash
rg --fixed-strings 'user.email' .
```

Fallback:

```bash
grep -R --line-number --fixed-strings 'user.email' .
```

Use `--fixed-strings` (`-F`) for user-provided text that should not be interpreted as a regular expression, such as punctuation-heavy strings, URLs, stack traces, or snippets containing brackets.

### Case sensitivity

```bash
rg --ignore-case 'todo' .
rg --case-sensitive 'TODO' .
rg --smart-case 'error' .
```

Fallbacks:

```bash
grep -Ri --line-number 'todo' .
grep -R --line-number 'TODO' .
```

`rg` is case-sensitive by default. Use explicit flags in shared commands when case behavior matters.

### Limit matches by file type or glob

```bash
rg --type rust 'Result<' .
rg --type-add 'vue:*.vue' --type vue 'defineProps' .
rg --glob '*.test.ts' 'render\(' .
rg --glob '!dist/**' --glob '!node_modules/**' 'pattern' .
```

Fallback examples:

```bash
find . -name '*.rs' -type f -exec grep -n 'Result<' {} +
find . -name '*.test.ts' -type f -exec grep -n 'render(' {} +
```

Use `rg --type-list` to see built-in file types. Prefer `--type` and `--glob` over piping through file filters because pruning during traversal is faster and avoids irrelevant files.

### Include hidden, ignored, or binary files

```bash
rg --hidden 'pattern' .
rg --no-ignore 'pattern' .
rg --unrestricted 'pattern' .
rg --text 'pattern' binary-or-unknown-file
```

- `--hidden` includes dotfiles and dot directories.
- `--no-ignore` includes paths ignored by `.gitignore`, `.ignore`, `.rgignore`, or global ignore files.
- `--unrestricted` (`-u`) relaxes hidden, ignored, and binary filtering as it is repeated.
- `--text` searches binary files as if they were text.

Fallbacks usually need explicit path pruning or inclusion logic because `grep -R` does not respect ignore files by default.

### Show file names, counts, or matching lines only

```bash
rg --files-with-matches 'pattern' .
rg --files-without-match 'pattern' .
rg --count 'pattern' .
rg --count-matches 'pattern' .
rg --only-matching 'version = "[^"]+"' Cargo.toml
```

Fallback examples:

```bash
grep -R --files-with-matches 'pattern' .
grep -R --files-without-match 'pattern' .
grep -R --count 'pattern' .
```

Use `--count-matches` when multiple matches on the same line should be counted separately; `--count` counts matching lines.

### Add context and control output

```bash
rg --line-number --column 'pattern' .
rg --before-context 2 --after-context 3 'pattern' .
rg --context 3 'pattern' .
rg --heading --line-number 'pattern' .
rg --no-heading --line-number 'pattern' .
```

Fallback examples:

```bash
grep -R -n -C 3 'pattern' .
grep -R -n -B 2 -A 3 'pattern' .
```

Use `--vimgrep` when output should be easy to send to editors or quickfix lists:

```bash
rg --vimgrep 'pattern' .
```

### Search multiline patterns

```bash
rg --multiline 'function\s+\w+\([^)]*\)\s*\{' .
rg --multiline --multiline-dotall 'start.*end' .
```

Use multiline search only when needed because it can be more expensive and changes how `.` and anchors behave. Add `--multiline-dotall` when `.` should match newlines.

### Search compressed or encoded files

```bash
rg --search-zip 'pattern' logs/
rg --encoding utf-16le 'pattern' file.txt
```

Use `--search-zip` for archives and compressed files supported by ripgrep. If results look garbled or missing in non-UTF-8 files, specify `--encoding`.

### List searchable files

```bash
rg --files .
rg --files --glob '*.md' .
rg --files --hidden --no-ignore .
```

Fallback:

```bash
find . -type f
```

Use `rg --files` when the task is file listing filtered by ripgrep's ignore semantics. Use `fd` when the task is primarily finding paths by name, extension, type, size, or modification time.

### Replace in output, not in files

```bash
rg 'oldName' --replace 'newName' .
```

`--replace` changes the displayed matches only; it does not edit files. For actual file edits, use a dedicated editor, script, or the code-editing tool after reviewing matches.

### Machine-readable output

```bash
rg --json 'pattern' .
```

Use `--json` for scripts that need stable structured data. Avoid parsing colored human output; add `--color never` if plain text is required.

### Safe piping and batch execution

For filenames that may contain spaces or newlines, use NUL-delimited output:

```bash
rg --files-with-matches --print0 'pattern' . | xargs -0 grep -n 'other-pattern'
```

For search results with line content, prefer `--json` over ad hoc parsing when correctness matters.

## Choosing rg vs grep

Prefer `rg` for:

- Searching file contents in repositories, large directory trees, logs, books, or document exports.
- Finding definitions, references, TODOs, errors, literals, regex matches, or multiline patterns.
- Searches that should respect `.gitignore` and skip generated or vendor directories by default.
- Filtering by file type, glob, context, counts, matching files, or structured JSON output.
- Feeding match lists into `fzf`, `xargs`, editors, scripts, review tools, or refactoring workflows.

Use `grep` for:

- Systems where `rg` is not installed and installing is out of scope.
- Strict POSIX shell scripts that must work without extra dependencies.
- Very small one-file searches where `grep` is already sufficient and portability is more important.
- Environments with a required grep-specific option or behavior.

## Choosing rg vs fd

Use `rg` when the user wants to search inside files. Use `fd` when the user wants to find file or directory names. Combine them when useful:

```bash
fd --extension ts . src | xargs rg 'pattern'
```

Usually prefer pure `rg` filters first because they let ripgrep prune traversal itself:

```bash
rg --type ts 'pattern' src
```

## Troubleshooting

- If `rg` returns fewer results than expected, check hidden and ignore behavior first; try `--hidden`, `--no-ignore`, or `--unrestricted`.
- If punctuation-heavy text fails to match, use `--fixed-strings`.
- If a pattern begins with a dash, use `rg -e '-pattern'` or `rg -- '-pattern'`.
- If shell quoting breaks the pattern, wrap it in single quotes in POSIX-like shells and escape embedded single quotes carefully.
- If a regex feature is unsupported, try `--pcre2` when available.
- If output is too noisy, narrow the path, add `--type`, add `--glob`, or use `--files-with-matches`.
- If output order matters, sort explicitly: `rg ... | sort`.
- If a command will pass paths to another tool, prefer `--print0` with `xargs -0` when supported.

## Response style

When helping with `rg`:

1. Give the `rg` command first when the user asks for a command.
2. Include a `grep` fallback when the user needs portability or when `rg` may not be installed.
3. Briefly explain the options that affect matching scope: regex vs literal, case sensitivity, hidden/ignored files, type/glob filters, and context.
4. Prefer narrowing by path, `--type`, or `--glob` before piping through slower filters.
5. Do not run broad or expensive searches from filesystem root; search from `.` or a specific path.
6. For risky follow-up actions based on matches, first show or summarize the matches and ask for confirmation before executing destructive commands.
