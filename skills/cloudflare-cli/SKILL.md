---
name: cloudflare-cli
description: Use this skill whenever the user wants to inspect, manage, script, or automate Cloudflare resources from the command line; compose, debug, or explain Cloudflare cf commands; or work with Cloudflare DNS records, zones, Workers, Pages, R2 buckets and objects, KV namespaces, D1 databases, queues, routes, profiles, or authentication. Also use it before writing shell scripts or CI steps that call Cloudflare's cf CLI, even if the user does not explicitly say "cloudflare-cli". Prefer verified cf commands for Cloudflare resource operations. Do not use this skill for the unrelated Cloud Foundry cf CLI or purely application-code tasks that do not need Cloudflare CLI operations.
compatibility: Requires Cloudflare's `cf` CLI; most resource commands require configured authentication. Examples verified with 1.0.0-beta.14; check installed command help because the CLI is evolving. Shell examples assume a POSIX-like shell unless specified otherwise.
license: Apache-2.0
---

# cloudflare-cli

Use Cloudflare's `cf` CLI for shell-based resource inspection and management. Discover the installed command before composing it: this CLI has its own command paths and options, not Wrangler's or the AWS CLI's.

## Start with availability and target identity

```bash
command -v cf >/dev/null 2>&1
cf --version
```

Verify that `cf` is Cloudflare's CLI, not Cloud Foundry's executable with the same name. If uncertain, inspect `cf --help` once. If missing or conflicting, explain the prerequisite and ask the user to resolve it; do not silently install software or substitute another CLI.

When account access is authorized, check authentication before resource operations:

```bash
cf auth whoami --profile staging
```

- Confirm the intended profile, account, and zone; a profile name is not proof of the target account. Do not guess an account-selection flag.
- If authentication is missing or expired, have the user perform `cf auth login --profile staging`. In Claude Code, suggest `! cf auth login --profile staging` so interactive output stays in the session. Do not silently start login, force reauthentication, log out, or change stored credentials.
- Never request tokens in chat, print secret-bearing configuration, or include credentials in examples. Use existing approved credential sources.
- For a command-only request or an explicit offline constraint, propose identity checks rather than accessing the account.

## Discover commands by intent

Start command discovery with an anonymous description of the action and resource type:

```bash
cf cli search "list DNS records"
```

Search queries must not contain names, domains, email addresses, account/resource IDs, tokens, or other identifying values. Discovery may contact a service; keep identifiers in the eventual resource command, not the search query. If network access is forbidden, use supplied help fixtures or explain which discovery command the user should run later.

Pick the best of the five compact JSON matches instead of repeating similar searches. Then inspect that specific command:

```bash
cf dns records list --help
cf schema dns records list
```

For API details, replace the discovered command's leading `cf` with `cf schema`. Do not enumerate the tree by chaining nested `--help` calls. Reuse verified help for the same installed version rather than rediscovering it for every invocation.

Schema output describes the HTTP method, endpoint, path/query parameters, and available body fields. It is not always exhaustive: beta14's DNS creation schema reports an empty `requestBodyFields` array while command help accepts `--body`. Consult the corresponding Cloudflare API documentation for missing payload details; do not invent individual flags or interpret an empty schema as proof that no body is needed.

## Command shape and scope

```bash
cf <command path> [positionals] [options]
```

Important global options:

- `--profile <profile>` selects an authentication profile.
- `--zone <zone-id-or-domain>` (`-z`) selects a zone and overrides `CLOUDFLARE_ZONE_ID`. Use it explicitly for zone operations when the target could be ambiguous.
- `--mode <mode>` selects the mode used to evaluate project configuration. Inspect configuration before choosing one; it is not an AWS-style region selector.
- `--local` requests local resource simulations; confirm support for the selected command. It does not make every command safe or side-effect-free.
- `--persist-to <directory>` selects local persisted-state storage.
- `--quiet` suppresses non-essential output; it is not a JSON-format switch.

Do not borrow `--account-id`, `--json`, `--output`, AWS `--query`, or Wrangler flags unless this installed command documents them. Account-scoped endpoints still need a verified account even when no account flag appears in help.

## Common command patterns

The examples below are templates, not permission to execute them. Replace example targets only with verified user-supplied values.

### DNS inspection and changes

Use explicit server-side filters rather than the loosely defined `--search` option for automation:

```bash
cf dns records list --zone example.com --profile staging \
  --type A --proxied true --match all --page 1 --per-page 100

cf dns records list --zone example.com --profile staging \
  --name api.example.com --type A --match all
```

`--name` is an exact-name filter; `--name-contains` is a substring filter. Keep combined filters deterministic with `--match all` when all conditions must hold.

DNS create/edit/update accepts a raw JSON `--body`. Verify the current API body requirements and inspect existing records first to avoid conflicts or duplicates. For example, after confirming the zone and desired DNS-only A record:

```bash
# Preview only; do not run without authorization for the preview.
cf dns records create --zone example.com --profile staging \
  --body '{"type":"A","name":"api.example.com","content":"192.0.2.10","ttl":300,"proxied":false}' \
  --dry-run
```

The payload illustrates standard DNS record fields; check the current DNS API documentation if schema discovery omits them. Ask for missing record type, content, zone, TTL, or proxy intent rather than guessing operational values. JSON booleans are unquoted; shell-quote the whole JSON string. For user-controlled values, use a JSON serializer rather than interpolating text into JSON.

After explicit authorization, the same command without `--dry-run` creates the record. `cf dns records edit <dns-record-id>` updates an existing record; `cf dns records update <dns-record-id>` is described as overwriting it. Inspect help/schema and existing state before choosing either; do not assume omitted fields are preserved by an overwrite. A/AAAA and CNAME records cannot coexist at the same name; NS has additional exclusivity constraints.

### KV namespaces

```bash
cf kv namespaces list --profile staging --page 1 --per-page 100
```

Discover key/value operations separately. Do not assume their arguments match namespace operations or Wrangler's `kv` commands. Values may contain secrets; avoid dumping them unnecessarily.

### D1 SQL

```bash
cf d1 query '<database-id>' --profile staging \
  --sql 'SELECT name FROM sqlite_master WHERE type = '\''table'\'' LIMIT 20;'
```

`database-id` is positional. The command also documents `--params`, `--batch`, and `--body`; inspect their help/schema before constructing complex or parameterized queries. `--batch` accepts a JSON array or `@path/to/file.json` according to beta14 help; do not assume all body options support the same file syntax.

Classify risk by every SQL statement, not by the word `query` or the API's POST method. A bounded SELECT can be read-only; INSERT, UPDATE, DELETE, schema changes, mutating PRAGMAs, and multi-statement batches may change data. Confirm the database/account and authorization before writes, and avoid exposing sensitive query results.

### R2 objects

```bash
cf r2 objects list --profile staging \
  --bucket-name example-archive --prefix 'reports/' --per-page 100

# Continue with the cursor returned by the preceding response.
cf r2 objects list --profile staging \
  --bucket-name example-archive --prefix 'reports/' --per-page 100 \
  --cursor '<returned-cursor>'
```

Repeat with each returned cursor until the response indicates exhaustion. Preserve bucket, prefix, profile, and any jurisdiction options between requests. `--start-after` is a lexicographic key boundary, not a substitute for the returned pagination cursor. `--delimiter` groups keys and may change what is returned; do not add it when the task is to inventory every object.

R2 command help recommends the S3-compatible API or Worker bindings for most workloads. Mention those when appropriate for application integration or large transfers; do not invent `cf` transfer/sync commands or silently switch credential systems.

## Pagination and output

Pagination is command-specific:

- DNS record and KV namespace listing document `--page` and `--per-page`.
- R2 object listing documents `--cursor` and `--per-page`.

Do not claim the CLI automatically retrieves all pages. Inspect actual response pagination information before implementing loops, and never call a first-page result a complete inventory. In offline answers, explain the continuation mechanism without guessing response field names.

Inspect actual output before writing `jaq`/`jq` selectors. Do not assume every command returns the same envelope, or that `--quiet` removes all non-JSON output. Keep stderr separate and check command exit status before treating an empty result as success. If output contains tokens, secrets, personal information, or object contents, redact or summarize it.

## Worker development and deployment

Inspect the project configuration, scripts, target profile, and mode before proposing build/dev/deploy commands. Discover additional project commands with `cf cli search` and check their selected help; do not transplant a Wrangler workflow.

```bash
cf deploy --help
cf deploy --profile staging --dry-run
```

`cf deploy --dry-run` builds the project and runs checks without uploading the Worker. It may still run project code and write local build outputs, so it is not a universally side-effect-free operation.

- Deployment changes live code; show the target and command and obtain authorization before running it.
- Beta14 documents automatic binding-resource provisioning with `--provision` defaulting to true. Inspect required resources and cost implications rather than assuming deployment only uploads code.
- `--prebuilt` deploys existing Build Output Specification files without building; inspect those artifacts first.
- `--secrets-file` can upload secrets with a version. Do not display its contents, commit it, or pass it to an unintended target.
- Inspect how project configuration maps modes and resources; do not assume a mode called staging guarantees a non-production destination.

## Safety and troubleshooting

For changes, verify the profile/account, zone or resource ID, current state, and requested outcome. Show the exact proposed command and explain its scope before execution. Obtain clear authorization for creates, updates, deletes, deployments, permission/security changes, and production operations; do not treat discovery or preview authorization as permission to mutate.

Use `--dry-run` only where selected command help documents it. A preview is not proof of live permission checks, successful execution, or rollback safety. Avoid blind retries of writes because the first request may already have succeeded. Read back the relevant state after an authorized change when appropriate.

- **Unknown command/option:** check the installed version, repeat anonymous intent discovery if necessary, then inspect selected help. Do not add plausible-looking flags from another CLI.
- **Missing/expired credentials:** inspect authorized `cf auth whoami --profile ...`; have the user refresh login rather than handling credentials in chat.
- **Permission errors:** report the operation and verified target; do not broaden privileges or switch profiles silently.
- **Missing resources/empty results:** check account/profile, zone, resource IDs, filters, mode, and pagination before concluding the resource is absent.
- **Rejected JSON:** validate JSON syntax and current API requirements; schema body fields may be incomplete. Do not assume `@file` or `file://` works unless help documents it for that option.
- **Rate limits/transient failures:** respect retry information and use bounded backoff for safe reads; verify state before retrying mutations.

## Response style

1. Give the complete verified command first for command requests; use explicit scope where needed.
2. Briefly explain meaningful filters, pagination, body quoting, and target selection.
3. Separate read-only inspection, previews, and live mutations; state what was actually run.
4. Ask focused questions when target or payload details are missing instead of guessing them.
5. For offline requests, provide a command plan and caveats, not fabricated account results.
