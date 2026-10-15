import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_loop


class RunLoopDefaultTests(unittest.TestCase):
    def test_default_command_discovers_generated_top_level_test(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "test_counter.py").write_text(
                "import unittest\n"
                "class CounterTests(unittest.TestCase):\n"
                "    def test_count(self):\n"
                "        self.assertEqual(len('hello'), 5)\n",
                encoding="utf-8",
            )

            result = run_loop.subprocess.run(
                run_loop.DEFAULTS["test_command"],
                shell=True,
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Ran 1 test", result.stderr)

    def test_default_test_command_runs_unittest_after_successful_job(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            jobs = root / "jobs"
            jobs.mkdir()
            (jobs / "example.md").write_text("sample job", encoding="utf-8")

            with patch.object(run_loop, "HERE", root), patch.object(
                run_loop.sys, "argv", ["run_loop.py"]
            ), patch.object(
                run_loop, "run_shell", return_value=0
            ) as run_shell:
                result = run_loop.main()

            self.assertEqual(result, 0)
            self.assertEqual(run_shell.call_count, 2)
            self.assertEqual(
                run_shell.call_args_list[1].args[0],
                "python3 -m unittest discover -q",
            )
            records = [
                json.loads(line)
                for line in (root / "results/log.jsonl").read_text().splitlines()
            ]
            self.assertEqual(records[0]["status"], "green")
            self.assertEqual(records[0]["test_exit"], 0)


if __name__ == "__main__":
    unittest.main()
