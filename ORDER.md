# Long-term plan

Plan-Status: in_progress

## Purpose and destination

This plan serves the purpose stated in `README.md`: provide a small, free starter that lets a user run a Codex CLI job through implementation, tests, and a recorded result with one command. `run_loop.py` deliberately stays sequential and minimal; this plan does not add queueing, parallel execution, recovery services, or broader automation.

The destination is a starter whose documented one-command path is reproducibly checked from setup through a recorded result, whose bounded filesystem effects and failure behavior match its user-facing instructions, and whose small test suite can detect regressions in that path. This extends the existing purpose without changing the product's authority, operating budget, or scope.

## Current state and gap

- `README.md` documents a macOS/Linux one-line launch, Codex CLI and Python prerequisites, and says the starter creates `try-loop/`.
- `start.sh` downloads `run_loop.py` and a sample job into `try-loop/`, runs the job, retries once after failure, and reports the result location.
- `run_loop.py` processes jobs sequentially, runs the configured test command after a successful Codex command, and appends a JSONL result.
- `tests/test_start_retry.py` checks retry counts using stub executables; its stub `curl` creates empty files. `tests/test_run_loop.py` checks the default test command but mocks the job execution. The checked-in tests therefore do not exercise the successful setup-to-result path or verify the advertised filesystem boundary end to end.

## Priority, dependencies, and exit conditions

1. **MS-001 — verify the one-command success path locally.** Add a bounded test using stubbed tools in a temporary directory. It must execute the real `start.sh` success path, observe the expected result, and verify no files were created outside `try-loop/`. This is the next action and should fit about 30 minutes.
2. **MS-002 — verify driver result and failure behavior.** Exercise `run_loop.py` with stubbed Codex and test commands, checking result records, stop-on-failure behavior, and temporary prompt cleanup. Depends on MS-001 establishing the outer-path test fixture approach.
3. **MS-003 — reconcile user instructions with verified behavior.** Compare README's prerequisites, side-effect claim, success artifacts, and retry guidance against the script and the preceding tests; correct only mismatches and verify the referenced paths. Depends on MS-001 and MS-002.

The plan exits when these checks pass, README claims match the tested behavior, and the existing purpose remains satisfied. At that point, assess the purpose against the evidence before adding any further milestone; if the whole purpose is achieved, record `Plan-Status: achieved`. Do not add work solely to keep the plan populated.
