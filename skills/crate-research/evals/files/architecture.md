# Parcelwatch architecture

Build a local-first command-line tool in Rust for inspecting application logs.

## Product boundaries

- Linux and macOS; stable Rust; a single executable.
- Users run `parcelwatch scan <path>` to filter log lines and `parcelwatch summarize <path>` to print counts.
- Both commands accept an optional severity filter; invalid severity values should produce a useful error and usage text.
- Missing required paths should show help. Support `--help` and `--version`.
- Read files as a stream; do not load entire logs into memory.
- No daemon, networking, GUI, or async requirement.

## Delivery

Implement the first vertical slice and tests. The architecture is approved; library choices have not been made. There is no existing argument parser or Cargo dependency policy beyond using permissive licenses.
