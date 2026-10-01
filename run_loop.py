#!/usr/bin/env python3
"""教育用スターターキット — 「ジョブ定義 → codexで実装 → テスト → 記録」の逐次ループ。

動画で紹介した自律ループの考え方を、公開されている Codex CLI だけで
手で試せるようにした**意図的に単純化した**ドライバです（逐次実行のみ・
キュー管理や並列実行・復旧処理は意図的に持ちません）。

使い方:
    python3 run_loop.py                 # jobs/ の .md を順に消化
    python3 run_loop.py --dry-run       # 実行せず対象ジョブだけ表示
設定は同じ dir の config.json（任意）:
    {"jobs_dir": "jobs",
     "codex_command": "codex exec -s workspace-write \"$(cat {job_file})\"",
     "test_command": "python3 -m pytest -q",
     "results_log": "results/log.jsonl",
     "stop_on_fail": true}
"""
import argparse
import json
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

DEFAULTS = {
    "jobs_dir": "jobs",
    "codex_command": 'codex exec -s workspace-write "$(cat {job_file})"',
    "test_command": "python3 -m pytest -q",
    "results_log": "results/log.jsonl",
    "stop_on_fail": True,
}


def load_config() -> dict:
    cfg = dict(DEFAULTS)
    cfg_file = HERE / "config.json"
    if cfg_file.exists():
        cfg.update(json.loads(cfg_file.read_text(encoding="utf-8")))
    return cfg


def run_shell(cmd: str) -> int:
    return subprocess.call(cmd, shell=True, cwd=HERE)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    cfg = load_config()

    jobs_dir = HERE / cfg["jobs_dir"]
    jobs = sorted(jobs_dir.glob("*.md"))
    if not jobs:
        print(f"ジョブがありません: {jobs_dir}/*.md")
        return 1
    print(f"対象ジョブ {len(jobs)} 件: " + ", ".join(f.name for f in jobs))
    if args.dry_run:
        return 0

    log_path = HERE / cfg["results_log"]
    log_path.parent.mkdir(parents=True, exist_ok=True)

    for job in jobs:
        print(f"\n=== {job.name} ===")
        started = time.time()
        # コマンドテンプレートに job_file を差し込む。shlex.quote で
        # ファイル名に空白等があっても安全に。
        with tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, encoding="utf-8"
        ) as tmp:
            tmp.write(job.read_text(encoding="utf-8"))
            tmp_path = tmp.name
        try:
            codex_cmd = cfg["codex_command"].format(
                job_file=shlex.quote(tmp_path))
            codex_rc = run_shell(codex_cmd)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        test_rc = None
        if cfg["test_command"] and codex_rc == 0:
            test_rc = run_shell(cfg["test_command"])

        duration = round(time.time() - started, 1)
        status = ("green" if codex_rc == 0 and (test_rc in (None, 0))
                  else "codex_fail" if codex_rc != 0 else "test_fail")
        record = {
            "job": job.name,
            "started_at": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "codex_exit": codex_rc,
            "test_exit": test_rc,
            "duration_s": duration,
            "status": status,
        }
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(f"結果: {status}（{duration}s・記録: {log_path.name}）")

        if status != "green" and cfg["stop_on_fail"]:
            print("失敗で停止（config.json の stop_on_fail で変更可）")
            return 1
    print("\n全ジョブ完了")
    return 0


if __name__ == "__main__":
    sys.exit(main())
