---
name: fd
description: Use this skill whenever the user wants to find files or directories by name, extension, glob, regex, type, size, modification time, or path; replace slow find commands or Glob/glob-style file discovery; compose, debug, or explain fd commands; or search filesystem entries before feeding them into tools like fzf, xargs, editors, formatters, or scripts. Prefer fd as the primary file-finder over find and generic glob discovery because it is faster, simpler, parallelized, and respects ignore files by default; fall back to POSIX find only when fd is unavailable or when a find-only predicate is required.
compatibility: Requires the fd CLI for preferred commands; if fd is not installed, fall back to find. Generated examples assume a POSIX-like shell unless the user specifies otherwise.
license: Apache-2.0
---

# fd

Use `fd` as the first-choice tool for filesystem entry discovery. It is usually much faster and easier to read than `find` or generic Glob/glob-style discovery, runs searches in parallel, skips hidden and ignored files by default, and has direct filters for common cases such as file type, extension, size, depth, and modification time. Fall back to `find` when `fd` is not installed, when strict POSIX portability matters, or when the task needs a predicate that `fd` does not support.

## Start with tool availability

Before running an `fd` command, check whether `fd` is available when the environment is uncertain:

```bash
command -v fd >/dev/null 2>&1
```

- If `fd` exists, use it for file and directory discovery.
- If `fd` is missing, use `find` and keep the fallback as close as practical to the intended `fd` behavior.
- If providing a reusable snippet, include a fallback only when useful; otherwise mention that `find` is the fallback.

## Command shape

`fd` uses this basic form:

```bash
fd [OPTIONS] [pattern] [path]...
```

Important differences from `find`:

- The pattern is a regular expression by default and matches the filename only.
- Add `--glob` (`-g`) for glob patterns.
- Add `--full-path` (`-p`) when the pattern should match the whole path.
- Search paths come after the pattern, or use `--search-path` for multiple explicit roots.
- Hidden files and ignored files are skipped by default.
- If a pattern starts with `-`, pass `--` before it: `fd -- '-foo'`.

## Common command patterns

### Find files by name

```bash
fd 'config' .
```

Fallback:

```bash
find . -name '*config*'
```

Use `--glob` when the user gives shell-style wildcards:

```bash
fd --glob '*.config.*' .
```

Fallback:

```bash
find . -name '*.config.*'
```

### Find only files, directories, or symlinks

```bash
fd --type file 'test' .
fd --type directory 'cache' .
fd --type symlink 'current' .
```

Short forms are fine in commands once clarity is established:

```bash
fd -tf 'test' .
fd -td 'cache' .
fd -tl 'current' .
```

Fallbacks:

```bash
find . -type f -name '*test*'
find . -type d -name '*cache*'
find . -type l -name '*current*'
```

### Find by extension

```bash
fd --type file --extension ts .
fd -tf -e ts -e tsx .
```

Fallback:

```bash
find . -type f \( -name '*.ts' -o -name '*.tsx' \)
```

When using `find` alternation, put longer extensions first when that avoids accidental early matches in regex-based forms.

### Include hidden or ignored files

```bash
fd --hidden 'env' .
fd --no-ignore 'generated' .
fd --unrestricted 'secret' .
```

- `--hidden` includes dotfiles and dot directories.
- `--no-ignore` includes paths ignored by `.gitignore`, `.ignore`, `.fdignore`, or global ignore files.
- `--unrestricted` (`-u`) combines hidden and ignored search; repeated `-u` can relax more restrictions in some fd versions.

Fallbacks usually need explicit pruning logic because `find` does not respect ignore files by default:

```bash
find . -name '*env*'
```

### Exclude noisy directories or patterns

```bash
fd --exclude node_modules --exclude .git --exclude dist 'pattern' .
```

Fallback:

```bash
find . \( -path '*/node_modules' -o -path '*/.git' -o -path '*/dist' \) -prune -o -name '*pattern*' -print
```

Use `--exclude` rather than shell pipes when the exclusion should affect traversal, because avoiding traversal is faster than filtering after the fact.

### Limit depth or result count

```bash
fd --max-depth 2 'README' .
fd --exact-depth 1 --type directory .
fd --max-results 20 'test' .
fd -1 'package.json' .
```

Fallbacks:

```bash
find . -maxdepth 2 -name '*README*'
find . -maxdepth 1 -type d
find . -name '*test*' | head -n 20
```

Prefer `fd -1` when only one match is needed; it quits early.

### Match full paths

```bash
fd --full-path --glob '**/.github/workflows/*.yml' .
```

Fallback:

```bash
find . -path '*/.github/workflows/*.yml'
```

Use `--full-path` for path fragments such as `src/**/test`, `.github/workflows`, or nested directory constraints. Without it, `fd` matches only the basename.

### Case sensitivity and literal strings

```bash
fd --case-sensitive 'Makefile' .
fd --ignore-case 'readme' .
fd --fixed-strings '[draft]' .
```

`fd` uses smart case by default: lowercase patterns are case-insensitive, while uppercase characters make matching case-sensitive. Use `--fixed-strings` for user-provided text that should not be interpreted as a regular expression.

### Size and modification time filters

```bash
fd --type file --size +10m .
fd --type file --changed-within 2weeks .
fd --type file --changed-before '2026-01-01' .
```

Fallback examples:

```bash
find . -type f -size +10M
find . -type f -mtime -14
find . -type f ! -newermt '2026-01-01'
```

Mention that date parsing varies more across `find` implementations than across `fd` versions.

### Safe piping and batch execution

For filenames that may contain spaces or newlines, use NUL-delimited output:

```bash
fd --type file --extension jpg --print0 . | xargs -0 file
```

Use `--exec` for one command per result and `--exec-batch` for one or more batched commands:

```bash
fd -e zip --exec unzip
fd -e rs --exec-batch wc -l
```

The order of `--exec` and `--exec-batch` execution is not deterministic, so do not rely on result order for commands with side effects. For destructive or broad mutations, show the matching command first and ask for confirmation before executing.

## Choosing fd vs find or Glob

Prefer `fd` for:

- Finding files or directories by name, glob, regex, extension, type, size, depth, or modification time.
- Replacing broad Glob/glob-style file discovery when you need faster traversal, ignore-file handling, type filters, depth limits, or reusable shell commands.
- Searching repositories where `.gitignore` behavior is desirable.
- Large trees where `find` would be slow.
- Feeding file lists into `fzf`, `xargs`, editors, formatters, or analysis scripts.
- Clear command snippets for humans to read and modify.

Use `find` for:

- Systems where `fd` is not installed and installing is out of scope.
- Strict POSIX shell scripts that must work without extra dependencies.
- Find-specific predicates or actions not available in `fd`.
- Cases where default `find` behavior of including ignored and hidden files is explicitly desired and easier to express.

## Troubleshooting

- If `fd` returns fewer results than expected, check hidden and ignore behavior first; try `--hidden`, `--no-ignore`, or `--unrestricted`.
- If a glob does not match, add `--glob`; otherwise `fd` treats the pattern as a regex.
- If a directory fragment does not match, add `--full-path`.
- If a pattern begins with a dash, use `fd -- '-pattern'`.
- If output order matters, sort explicitly: `fd ... | sort`.
- If the command will pass paths to another tool, prefer `--print0` with `xargs -0` when supported.

## Response style

When helping with `fd`:

1. Give the `fd` command first when the user asks for a command or when filesystem discovery would otherwise use `find` or a broad Glob/glob-style search.
2. Include a `find` fallback when the user needs portability or when `fd` may not be installed.
3. Briefly explain the options that affect matching scope: regex vs glob, basename vs full path, hidden/ignored files, and type filters.
4. Avoid running destructive `--exec` commands without explicit confirmation; for risky commands, first print or preview the matched paths.
