# daedal-skills

[![skills.sh](https://skills.sh/b/unive3sal/daedal-skills)](https://skills.sh/unive3sal/daedal-skills)

A collection of reusable skills for AI coding agents.

## Skills

| Skill | Path | Description | Requirements |
| --- | --- | --- | --- |
| `fzf` | [`skills/fzf`](skills/fzf) | Compose, debug, and explain safe `fzf` commands for fuzzy file selection, interactive pickers, previews, key bindings, and shell workflows. | Requires the `fzf` CLI when running generated commands. |

## Install

Install all skills in this repository:

```bash
npx skills add unive3sal/daedal-skills
```

Install only the `fzf` skill:

```bash
npx skills add unive3sal/daedal-skills --skill fzf
```

Install directly from the skill path:

```bash
npx skills add https://github.com/unive3sal/daedal-skills/tree/main/skills/fzf
```

## Discoverability on skills.sh

`skills.sh` discovers GitHub-hosted skills through the `skills` CLI. Installs such as `npx skills add unive3sal/daedal-skills` report anonymous aggregate telemetry, which powers the skills.sh leaderboard and install badge.

## License

Apache-2.0. See [LICENSE](LICENSE).
