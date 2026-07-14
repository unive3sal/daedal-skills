# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repository is a collection of reusable skills for AI coding agents, published for discovery/install through `skills.sh` and the `skills` CLI.

## Structure

- `skills/<skill-name>/SKILL.md` contains each skill. Current skills are `aws-cli`, `fd`, `fzf`, `jaq`, and `ripgrep`.
- Each `SKILL.md` uses YAML frontmatter with at least `name`, `description`, `compatibility`, and `license`, followed by Markdown instructions.
- `README.md` is the public index: keep its skill table and install examples in sync whenever adding, removing, or renaming a skill.
- `.gitignore` ignores `.claude/` and `*-workspace/`; skill evaluation workspaces should stay untracked.

## Common commands

There is no project build, lint, or test suite configured in this repository. Validate changes by reading the Markdown and checking git status/diffs.

Install all skills from this repo:

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

## Skill authoring conventions

When creating or editing a skill:

- Match the existing style: pushy trigger-focused `description`, concise `compatibility`, `license: Apache-2.0`, then practical command guidance.
- Prefer fast modern CLIs in this collection while documenting fallbacks: `fd` -> `find`, `rg` -> `grep`, `jaq` -> `jq`.
- Include availability checks when the preferred CLI may not be installed.
- Put common command shapes and examples in the skill body rather than only in the frontmatter.
- For interactive or mutating tools, spell out when not to run commands silently and when to ask the user to execute or confirm them.
