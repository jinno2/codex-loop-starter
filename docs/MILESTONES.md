# Execution milestones

Long-term plan: [ORDER.md](../ORDER.md)

## MS-001: Verify the one-command success path locally
Outcome: The real `start.sh` success path is covered with local stub tools, records the expected sample result, and creates files only under `try-loop/`.
Acceptance: Add a bounded integration test and run `python3 -m unittest tests.test_start_retry -v`; the real `start.sh` reaches its success message, the expected files exist under the temporary `try-loop/`, and a before/after listing shows no created paths elsewhere in the temporary working directory.
Evidence: pending — no end-to-end success-path or filesystem-boundary evidence exists yet.
Status: planned
Depends: none.
Next: Add the temporary-directory stub fixture and assert the real script's successful setup, run, result, and write boundary; target about 30 minutes.

## MS-002: Verify driver results and failure behavior
Outcome: `run_loop.py` behavior is covered across successful job execution, test failure, stop-on-failure, result logging, and temporary prompt cleanup.
Acceptance: Run `python3 -m unittest tests.test_run_loop -v`; tests using stub commands verify JSONL fields and exit behavior for success and failure, and assert no temporary prompt file remains.
Evidence: pending — current tests mock `run_shell` for the job path and do not establish these end-to-end driver outcomes.
Status: planned
Depends: MS-001's temporary-directory stub fixture approach.
Next: Extend the driver tests with stub commands and success/failure cases after MS-001.

## MS-003: Reconcile README claims with verified behavior
Outcome: The one-line setup instructions, prerequisites, filesystem-boundary claim, generated artifacts, and retry guidance match the scripts and tested behavior.
Acceptance: Review `README.md` against `start.sh`, `run_loop.py`, and tests; run `python3 -m unittest discover -v`; every repository-relative source link resolves, generated artifact paths are verified in the temporary test directory, and each behavioral claim is supported by code or an explicit test.
Evidence: pending — the current README and scripts are the source inputs; end-to-end evidence is pending MS-001 and MS-002.
Status: planned
Depends: MS-001 and MS-002.
Next: Make only evidence-backed README corrections and confirm all referenced paths after both test milestones pass.
