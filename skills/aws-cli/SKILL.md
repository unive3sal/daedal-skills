---
name: aws-cli
description: Use this skill whenever the user wants to inspect, manage, script, or automate anything in AWS from the command line; compose, debug, or explain aws commands; query or filter AWS API responses; or mentions AWS services or resources such as S3 buckets, EC2 instances, Lambda functions, IAM users and roles, CloudFormation stacks, CloudWatch logs and metrics, DynamoDB tables, ECS, EKS, SQS, SNS, Route 53, regions, profiles, or credentials, even if they never say "aws cli" explicitly. Also use it before writing shell scripts or CI steps that call aws, and when choosing between aws s3 and aws s3api or between server-side filters and client-side --query filtering.
compatibility: Requires the AWS CLI v2 (`aws`); most commands also require configured credentials. Generated examples assume a POSIX-like shell unless the user specifies otherwise.
license: Apache-2.0
---

# aws-cli

Use the `aws` CLI as the first-choice tool for inspecting and managing AWS resources from the shell. It covers every AWS service with a uniform shape, supports powerful client-side filtering with JMESPath, and paginates large result sets automatically. The same command patterns work interactively and in scripts, so prefer composing precise `aws` commands over ad-hoc console instructions or SDK one-off scripts.

## Start with tool availability and identity

Before running commands, check that the CLI exists and that credentials resolve, because most failures are environment problems rather than command problems:

```bash
command -v aws >/dev/null 2>&1
aws --version
aws sts get-caller-identity
```

- `aws sts get-caller-identity` is cheap, read-only, and confirms which account and principal the commands will act as. Run it first whenever the target account matters or credentials are uncertain.
- If it fails with an SSO or expired-token error, run `aws sso login --profile <profile>` (SSO profiles) or refresh the credentials source before retrying.
- If `aws` is missing, tell the user how to install it (`brew install awscli` on macOS, or the AWS installer packages) rather than silently falling back to raw HTTP calls.

## Command shape

```bash
aws [global options] <service> <operation> [parameters]
```

- Discover operations with the built-in help: `aws <service> help`, `aws <service> <operation> help`.
- Operation names map 1:1 to AWS API actions in kebab-case (`DescribeInstances` → `describe-instances`), so API documentation translates directly.
- Parameters that take structures accept shorthand (`Key=Name,Values=web`) or JSON. Load long values from files with `file://params.json`, and raw binary with `fileb://blob.bin`.
- Generate a parameter template with `--generate-cli-skeleton`, fill it in, and pass it back with `--cli-input-json file://input.json` for complex calls.

## Non-interactive output (important in scripts and agents)

AWS CLI v2 pipes output through a pager, which can hang non-interactive sessions. Disable it when running commands programmatically:

```bash
aws ec2 describe-instances --no-cli-pager
# or once per environment:
export AWS_PAGER=""
```

Pick the output format for the consumer:

```bash
aws ec2 describe-instances --output json    # default, best for jq/jaq
aws ec2 describe-instances --output table   # human-readable summaries
aws ec2 describe-instances --output text    # tab-separated, best for shell loops
aws ec2 describe-instances --output yaml
```

## Filtering: server-side filters vs --query

Combine both: server-side `--filters` reduce what the API returns; client-side `--query` (JMESPath) reshapes what the CLI prints. Prefer server-side filtering first because it is faster and avoids pagination over irrelevant data.

```bash
# Server-side: only running instances tagged env=prod
aws ec2 describe-instances \
  --filters 'Name=instance-state-name,Values=running' 'Name=tag:env,Values=prod' \
  --query 'Reservations[].Instances[].{ID:InstanceId,Type:InstanceType,IP:PrivateIpAddress,Name:Tags[?Key==`Name`]|[0].Value}' \
  --output table
```

JMESPath essentials for `--query`:

- `[]` flattens nested lists: `Reservations[].Instances[]`.
- `{Alias:Path}` builds objects; combine with `--output table` for readable columns.
- `[?Field=='value']` filters; literal strings use backticks or single quotes inside the expression.
- `| [0]` takes the first element of a filtered result.
- Quote the whole expression in single quotes so the shell does not interpret backticks.

For anything JMESPath makes painful, output JSON and pipe to `jq`/`jaq` instead of fighting the query syntax.

## Profiles and regions

Every command resolves an account and region; make them explicit when there is any ambiguity:

```bash
aws s3 ls --profile prod --region eu-west-1
```

- `--profile` selects a named profile from `~/.aws/config` / `~/.aws/credentials`; `AWS_PROFILE` sets it for a session.
- `--region` overrides the profile's region; `AWS_REGION` sets it for a session.
- List configured profiles with `aws configure list-profiles`, and inspect resolution with `aws configure list`.
- When the user has multiple accounts, confirm the target with `aws sts get-caller-identity` before mutating anything.

## Pagination

The CLI auto-paginates list/describe operations, which is usually what you want. Control it when result sets are large:

```bash
aws s3api list-objects-v2 --bucket my-bucket --max-items 100
aws logs describe-log-groups --page-size 50
aws ec2 describe-snapshots --no-paginate
```

- `--max-items` caps the total results (a `NextToken` is printed for resuming).
- `--page-size` changes the per-request size without changing the total (useful to avoid API throttling).
- `--no-paginate` makes exactly one API call.

## s3 vs s3api

- `aws s3` provides high-level file-manager commands: `ls`, `cp`, `mv`, `rm`, `sync`. Use it for transfers; it handles multipart uploads and recursion automatically.
- `aws s3api` exposes the raw S3 API: bucket policies, versioning, lifecycle, object metadata, presigned-adjacent operations. Use it when the high-level commands cannot express the operation.

```bash
aws s3 ls s3://my-bucket/prefix/
aws s3 cp ./report.pdf s3://my-bucket/reports/
aws s3 sync ./site s3://my-bucket --delete --dryrun   # preview first, then drop --dryrun
aws s3api get-bucket-versioning --bucket my-bucket
aws s3 presign s3://my-bucket/report.pdf --expires-in 3600
```

## Common command patterns

```bash
# Who am I / which account?
aws sts get-caller-identity

# Tail CloudWatch logs live
aws logs tail /aws/lambda/my-fn --follow --since 30m

# Invoke a Lambda and read the response
aws lambda invoke --function-name my-fn \
  --payload '{"key":"value"}' --cli-binary-format raw-in-base64-out /dev/stdout

# CloudFormation stack status
aws cloudformation describe-stacks --stack-name my-stack \
  --query 'Stacks[0].StackStatus' --output text

# Wait for an async operation to finish before continuing a script
aws ec2 wait instance-running --instance-ids i-0123456789abcdef0
aws cloudformation wait stack-create-complete --stack-name my-stack
```

Waiters (`aws <service> wait <condition>`) poll until a state is reached and exit non-zero on failure or timeout; prefer them over hand-rolled sleep loops in scripts.

## Safety with mutating commands

Read operations (`describe-*`, `list-*`, `get-*`) are safe to run freely. For anything that creates, modifies, or deletes resources:

- Show the exact command and ask the user to confirm before executing deletes, terminations, policy changes, or anything affecting production (`terminate-instances`, `delete-*`, `s3 rm --recursive`, `s3 sync --delete`, `put-*-policy`).
- Preview first where the service supports it: `--dryrun` for `aws s3` transfer commands, `--dry-run` for many EC2 operations (exits with `DryRunOperation` when the call would have succeeded).
- Scope the blast radius: list the resources a command will touch (`aws s3 rm s3://bucket/prefix --recursive --dryrun`) before running the real thing.
- Never guess account or region for a mutation; verify with `aws sts get-caller-identity` and an explicit `--region`.

## Troubleshooting

- **Command hangs in a script or agent**: the pager is waiting for input; add `--no-cli-pager` or set `AWS_PAGER=""`.
- **`Unable to locate credentials`**: no credential source resolved; check `aws configure list`, `AWS_PROFILE`, or run `aws sso login`.
- **`ExpiredToken` / SSO errors**: refresh with `aws sso login --profile <profile>` or re-export temporary credentials.
- **`AccessDenied`**: the principal from `aws sts get-caller-identity` lacks the IAM permission named in the error; report the action and principal rather than retrying blindly.
- **Empty results that should not be empty**: check the region first (`--region`), then whether a server-side filter or `--query` expression is wrong; drop `--query` to inspect the raw response.
- **`Invalid JMESPath` or shell mangling**: single-quote the whole `--query` expression; backticks inside must not be escaped by the shell.
- **Throttling (`Rate exceeded`)**: lower `--page-size`, add retries via `AWS_MAX_ATTEMPTS` and `AWS_RETRY_MODE=adaptive`.
- **Binary payload errors on Lambda/Kinesis**: pass `--cli-binary-format raw-in-base64-out` or use `fileb://`.

## Response style

When helping with the AWS CLI:

1. Give the complete `aws` command first, with explicit `--region`/`--profile` when the target is ambiguous.
2. Use `--query` plus `--output table` or `text` to make results directly readable instead of dumping raw JSON at the user.
3. For scripts, include `--no-cli-pager`, prefer `--output text` or JSON piped to `jq`/`jaq`, and use waiters instead of sleep loops.
4. Run read-only commands to gather facts, but show mutating or destructive commands and get confirmation before executing them.
