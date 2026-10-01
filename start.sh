#!/usr/bin/env bash
# codex-loop-starter — 1行スターター（非エンジニア向け・one-liner ブランチ）
#
# 何をするか（透明性のための説明）:
#   1. codex / python3 があるか確認する
#   2. 今いる場所に try-loop/ フォルダを作る
#   3. このリポジトリからドライバとサンプルジョブをダウンロードする
#   4. codex にサンプルの実装をさせて・テストを走らせ・結果を記録する
# あなたのPCの他のファイルには触れません。作るのは ./try-loop だけです。
set -euo pipefail

BRANCH=one-liner
BASE="https://raw.githubusercontent.com/jinno2/codex-loop-starter/$BRANCH"

say() { printf '\n%s\n' "$*"; }

command -v codex >/dev/null 2>&1 || {
  say "✗ codex コマンドが見つかりません。"
  say "  まず Codex CLI をインストールして認証（codex login）してください。"
  say "  手順: https://github.com/openai/codex"
  exit 1
}
PY="$(command -v python3 || command -v python || true)"
[ -n "$PY" ] || {
  say "✗ python3（または python）が見つかりません。"
  say "  インストール: https://www.python.org/downloads/"
  exit 1
}
command -v curl >/dev/null 2>&1 || {
  say "✗ curl が見つかりません。インストールしてから再実行してください。"
  exit 1
}

DIR=try-loop
mkdir -p "$DIR/jobs" "$DIR/results"
curl -fsSL "$BASE/run_loop.py" -o "$DIR/run_loop.py"
curl -fsSL "$BASE/jobs/example-job.md" -o "$DIR/jobs/example-job.md"

say "=== 準備OK: ./$DIR にサンプルジョブを用意しました ==="
say "これから codex が「文字計数ツール」を実装し、テストが走ります（数分かかります）"
cd "$DIR"
"$PY" run_loop.py

say ""
say "=== 完了! ==="
say "作られたファイル: $(pwd)/counter.py と test_counter.py（サンプルの成果物）"
say "実行の記録:       $(pwd)/results/log.jsonl"
say "確かめたら、このフォルダごと削除して大丈夫です。"
