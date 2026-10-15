import os
import subprocess
import tempfile
import unittest
from pathlib import Path


START_SH = Path(__file__).resolve().parents[1] / "start.sh"


class StartRetryTests(unittest.TestCase):
    def run_start(self, outcomes):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bindir = root / "bin"
            bindir.mkdir()
            count = root / "python-count"
            outcomes_file = root / "outcomes"
            outcomes_file.write_text(" ".join(map(str, outcomes)))

            codex = bindir / "codex"
            codex.write_text("#!/bin/sh\nexit 0\n")
            curl = bindir / "curl"
            curl.write_text('#!/bin/sh\nwhile [ "$#" -gt 0 ]; do\n'
                            '  if [ "$1" = "-o" ]; then shift; : > "$1"; exit 0; fi\n'
                            '  shift\ndone\nexit 1\n')
            python = bindir / "python3"
            python.write_text(
                '#!/bin/sh\n'
                f'count_file={str(count)!r}\n'
                f'outcomes_file={str(outcomes_file)!r}\n'
                'n=0; [ ! -f "$count_file" ] || n=$(cat "$count_file")\n'
                'n=$((n + 1)); echo "$n" > "$count_file"\n'
                'set -- $(cat "$outcomes_file")\n'
                'i=1; while [ "$i" -lt "$n" ]; do shift; i=$((i + 1)); done\n'
                'exit "${1:-1}"\n'
            )
            for command in (codex, curl, python):
                command.chmod(0o755)

            env = dict(os.environ, PATH=f"{bindir}:{os.environ['PATH']}")
            result = subprocess.run(
                ["bash", str(START_SH)], cwd=root, env=env,
                text=True, capture_output=True, check=False,
            )
            calls = int(count.read_text()) if count.exists() else 0
            return result, calls

    def test_retries_once_and_succeeds(self):
        result, calls = self.run_start([1, 0])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(calls, 2)
        self.assertIn("=== 完了! ===", result.stdout)

    def test_stops_after_two_failures(self):
        result, calls = self.run_start([1, 1])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(calls, 2)
        self.assertIn("2回とも失敗しました", result.stdout)


if __name__ == "__main__":
    unittest.main()
