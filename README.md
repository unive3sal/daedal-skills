# daedal-skills

[![skills.sh](https://skills.sh/b/unive3sal/daedal-skills)](https://skills.sh/unive3sal/daedal-skills)

A collection of reusable skills for AI coding agents.

## Skills

| Skill | Path | Description | Requirements |
| --- | --- | --- | --- |
| `aws-cli` | [`skills/aws-cli`](skills/aws-cli) | Compose, debug, and explain safe `aws` commands for inspecting, managing, and scripting AWS resources with JMESPath queries, profiles, regions, pagination, and waiters. | Requires the AWS CLI v2 (`aws`); most commands need configured credentials. |
| `fd` | [`skills/fd`](skills/fd) | Compose, debug, and explain fast `fd` commands for finding files and directories by name, glob, regex, type, size, time, or path. | Requires the `fd` CLI for preferred commands; falls back to `find` when unavailable. |
| `fzf` | [`skills/fzf`](skills/fzf) | Compose, debug, and explain safe `fzf` commands for fuzzy file selection, interactive pickers, previews, key bindings, and shell workflows. | Requires the `fzf` CLI when running generated commands. |
| `jaq` | [`skills/jaq`](skills/jaq) | Compose, debug, and explain fast `jaq` commands for querying, transforming, filtering, compacting, validating, and converting JSON-like structured data. | Requires the `jaq` CLI for preferred commands; falls back to `jq` when unavailable. |
| `ripgrep` | [`skills/ripgrep`](skills/ripgrep) | Compose, debug, and explain fast `rg` commands for searching text, codebases, logs, documents, definitions, references, and regex matches. | Requires the `rg` CLI for preferred commands; falls back to `grep` when unavailable. |

## Install

Install all skills in this repository:

```bash
npx skills add unive3sal/daedal-skills
```

Install a single skill:

```bash
npx skills add unive3sal/daedal-skills --skill aws-cli
npx skills add unive3sal/daedal-skills --skill fd
npx skills add unive3sal/daedal-skills --skill fzf
npx skills add unive3sal/daedal-skills --skill jaq
npx skills add unive3sal/daedal-skills --skill ripgrep
```

Install directly from a skill path:

```bash
npx skills add https://github.com/unive3sal/daedal-skills/tree/main/skills/aws-cli
npx skills add https://github.com/unive3sal/daedal-skills/tree/main/skills/fd
npx skills add https://github.com/unive3sal/daedal-skills/tree/main/skills/fzf
npx skills add https://github.com/unive3sal/daedal-skills/tree/main/skills/jaq
npx skills add https://github.com/unive3sal/daedal-skills/tree/main/skills/ripgrep
```

## Discoverability on skills.sh

`skills.sh` discovers GitHub-hosted skills through the `skills` CLI. Installs such as `npx skills add unive3sal/daedal-skills` report anonymous aggregate telemetry, which powers the skills.sh leaderboard and install badge.

## License

Apache-2.0. See [LICENSE](LICENSE).
