# Native integration matrix

This file is an execution plan, not a record of passing product tests. Source-inspection findings belong in `references/agent-loops.md`; recorded runs belong in the ignored workspace.

| Runtime | Installation / discovery to verify | Interaction and delegation checks | Execution status |
| --- | --- | --- | --- |
| Claude Code | Native project skill metadata is visible; skill body is loaded on invocation/read; inspect child roster separately | Interactive question path versus print/SDK host path; worker-to-parent report; actual human reply on continuation | Not run |
| Codex CLI | Native skill loader and implicit metadata matching; inspect child context rather than assuming inheritance | Mode-specific question availability; exec final pending result; command approval is not library selection | Not run |
| pi | Native skill metadata and explicit body loading; check enabled extensions | Built-in versus extension-provided tools; interactive UI versus print/RPC; no assumed built-in delegation | Not run |
| OpenCode | Current native skill tool and worker tool allowlist | Interactive questions versus noninteractive client handling; return blocker when child cannot question | Not run |

For each run use the exact source revision and installed version, not a generic product name. Separate behavior prescribed by a prompt from enforcement performed by the runtime.

## Required run record

```json
{
  "case_id": 1,
  "runtime": "<product>",
  "runtime_version": "<actual version>",
  "source_revision": "<SHA or unknown>",
  "model": "<actual model>",
  "interaction_mode": "<interactive/print/exec/RPC>",
  "permission_mode": "<actual mode>",
  "skill_visibility": "<parent and worker availability>",
  "configuration": "<original/revised>",
  "status": "<completed/infrastructure_error/not_run>",
  "first_skill_load_event": null,
  "first_affected_write_attempt_event": null,
  "human_decision_event": null,
  "result": "<pending/selected/failed/not_run>",
  "trace_path": "<full ordered event log>",
  "limitations": []
}
```

An unset event is not automatically failure or success: interpret it alongside runtime status. For example, no skill-load event after an authentication failure is an infrastructure error, while writing the parser without loading an exposed skill is an activation failure.
