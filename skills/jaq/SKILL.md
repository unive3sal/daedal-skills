---
name: jaq
description: Use this skill whenever the user wants to query, transform, filter, pretty-print, compact, validate, convert, or edit JSON-like structured data from files, stdin, command output, logs, APIs, or shell pipelines; compose, debug, port, or explain jq/jaq filters; extract fields, reshape arrays/objects, pass variables, slurp inputs, emit raw strings, update JSON in place, convert YAML/CBOR, or run jq-style tests. Prefer jaq as the first-choice JSON query tool because it is a fast jq-like CLI with familiar filter syntax and useful input/output format options. If jaq is unavailable, fall back to jq unless the user specifically needs a jaq-only feature.
compatibility: Requires the jaq CLI for preferred commands; if jaq is not installed, fall back to jq where the filter and options are compatible. Generated examples assume a POSIX-like shell unless the user specifies otherwise.
license: Apache-2.0
---

# jaq

Use `jaq` as the first-choice tool for querying and transforming JSON or JSON-like structured data. It follows jq-style filters, works well in shell pipelines, and supports common jq workflows such as raw output, compact output, slurping inputs, passing variables, and reading filters from files. Fall back to `jq` when `jaq` is not installed, when a system script must use an existing jq dependency, or when a jq-specific behavior is required.

## Start with tool availability

Before running a `jaq` command, check whether `jaq` is available when the environment is uncertain:

```bash
command -v jaq >/dev/null 2>&1
```

- If `jaq` exists, use it for JSON querying and transformation.
- If `jaq` is missing, use `jq` and keep the fallback as close as practical to the intended `jaq` behavior.
- If providing a reusable snippet, include a fallback only when useful; otherwise mention that `jq` is the fallback.

A reusable wrapper pattern is:

```bash
if command -v jaq >/dev/null 2>&1; then
  jaq '.items[] | .name' data.json
else
  jq '.items[] | .name' data.json
fi
```

## Command shape

`jaq` uses this basic form:

```bash
jaq [OPTION]... [FILTER] [ARG]...
command | jaq [OPTION]... [FILTER]
```

Important conventions:

- Quote filters with single quotes in shell examples to protect characters like `.`, `[]`, `{}`, `$`, and `|` from the shell.
- Positional arguments are input files by default.
- Use `-n` / `--null-input` when constructing JSON from scratch instead of reading input.
- Use `-R` / `--raw-input` when input is plain text rather than JSON.
- Use `-s` / `--slurp` when the filter needs all input values as one array.
- Use `-f` / `--from-file` for long filters or reusable filter files.

## Common command patterns

### Pretty-print or compact JSON

```bash
jaq '.' data.json
jaq --compact-output '.' data.json
```

Fallback:

```bash
jq '.' data.json
jq --compact-output '.' data.json
```

Use `--sort-keys` when stable object key order matters:

```bash
jaq --sort-keys '.' data.json
```

### Extract fields

```bash
jaq '.user.email' user.json
jaq -r '.user.email' user.json
jaq '.items[] | {id, name}' data.json
```

Use `-r` / `--raw-output` when the user wants strings without JSON quotes, such as values assigned to shell variables or written line-by-line.

### Filter arrays and objects

```bash
jaq '.items[] | select(.enabled == true)' data.json
jaq '.items[] | select(.name | test("^api-")) | .id' data.json
jaq '.items | map(select(.score >= 90))' data.json
```

Keep predicates inside the filter rather than post-processing JSON with text tools, because structural filtering avoids fragile parsing.

### Reshape data

```bash
jaq '{count: (.items | length), names: [.items[].name]}' data.json
jaq '.items | group_by(.type) | map({type: .[0].type, count: length})' data.json
jaq '.items | sort_by(.created_at) | reverse' data.json
```

Use object and array constructors when returning data to another program, and `-r` only at the boundary where plain text is required.

### Pass variables safely

```bash
jaq --arg name "$name" '.items[] | select(.name == $name)' data.json
jaq --argjson min_score "$min_score" '.items[] | select(.score >= $min_score)' data.json
```

Use `--arg` for strings and `--argjson` for numbers, booleans, arrays, objects, or null. Do not interpolate shell variables directly into filters.

### Read all inputs together

```bash
jaq --slurp 'add' part-*.json
jaq -s 'map(.items[]) | sort_by(.id)' shard-*.json
```

Use slurp when comparing, merging, sorting, or aggregating across multiple JSON documents.

### Process plain text input

```bash
printf '%s\n' alpha beta | jaq -R '{line: ., length: length}'
printf '%s\n' alpha beta | jaq -R -s 'split("\n")[:-1]'
```

Use `-R` for line-oriented text input. Combine `-R -s` when the filter should see the entire raw input as one string.

### Construct JSON from scratch

```bash
jaq -n --arg name "$name" --argjson count "$count" '{name: $name, count: $count}'
```

Use `-n` for scripts that need to emit JSON from shell variables without reading an input file.

### Convert input or output formats

```bash
jaq --from yaml '.' config.yaml
jaq --from yaml --to json '.' config.yaml
jaq --to yaml '.' data.json
```

Use format conversion only when the installed `jaq` supports the requested format. If falling back to `jq`, explain that jq does not provide the same built-in `--from` / `--to` format conversion and another tool may be needed.

### Edit files in place

```bash
jaq --in-place '.version = "2.0.0"' package.json
```

Before running broad or destructive in-place edits, inspect the target file and prefer a dry run without `--in-place`. Ask for confirmation when the edit affects many files or could overwrite user work.

### Run filter tests

```bash
jaq --run-tests tests.jq
```

Use this when the user is developing reusable filters and wants executable examples or regression tests.

## Choosing jaq vs jq

Prefer `jaq` for:

- Querying, filtering, transforming, compacting, or pretty-printing JSON.
- jq-style shell pipelines where performance and concise filters matter.
- Safe variable passing with `--arg`, `--argjson`, `--slurpfile`, or `--rawfile`.
- Built-in input/output format handling such as `--from yaml` or `--to yaml`, when supported.

Fall back to `jq` for:

- Systems where `jaq` is not installed.
- Existing scripts or CI jobs that intentionally depend on jq.
- Filters or options that rely on jq-specific semantics and have not been verified in jaq.

When compatibility matters, keep filters simple and test with the installed tool. Most common filters such as field access, `select`, `map`, object construction, `sort_by`, `group_by`, `length`, `keys`, `has`, and raw output are good candidates for either tool.

## Safety and robustness

- Treat JSON filters as code: quote them carefully and avoid shell interpolation.
- Use `--arg` or `--argjson` for user-provided values.
- Prefer structural JSON operations over `grep`, `sed`, or `awk` when parsing JSON.
- Do not use `--in-place` on important files until the non-mutating command produces the expected output.
- For command output, verify the producer emits valid JSON before assuming `jaq` can parse it.

## Response style

When helping with `jaq`:

1. Give the `jaq` command first when the user asks for a command.
2. Mention the `jq` fallback when portability or installation uncertainty matters.
3. Briefly explain the filter and only the options that matter for the task.
4. If a command mutates files with `--in-place`, say what will change and ask before running it unless the user explicitly authorized the edit.
