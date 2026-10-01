# codex-loop-starter

「**ジョブ定義 → codex で実装 → テスト実行 → 結果を記録**」という最小の
自律開発ループを、公開されている Codex CLI だけで手元で試せるキットです。

> **コマンド1行で試したい方（macOS / Linux）**: main ブランチの
> 1行スターター版へ → https://github.com/jinno2/codex-loop-starter
> この README（engineer ブランチ）はカスタマイズ前提のエンジニア向けです。

## 5分で試す

前提: [Codex CLI](https://github.com/openai/codex) がインストール済みで
`codex` コマンドが動く（OpenAI アカウントの認証・`codex login` 済み）こと。
git・python3（3.8+）も必要です。

```bash
git init try-loop && cd try-loop
KIT=<ダウンロードしたこのキットのパス>   # 例: ~/Downloads/codex-loop-starter
cp -r "$KIT/jobs" .
cp "$KIT/run_loop.py" .
python3 run_loop.py --dry-run      # 対象ジョブの確認
python3 run_loop.py                # 実行
cat results/log.jsonl              # 記録の確認
```

1ジョブごとに、ジョブ定義（`jobs/*.md` の中身）が codex に渡り、実装後に
テストが走り、結果が `results/log.jsonl` に1行ずつ記録されます。

## このキットの位置づけ

動画で紹介した運用の**考え方**を再現するための、意図的に単純化した教育用
ドライバです。キュー管理・並列実行・復旧処理など実運用向けの仕組みは
持たせていません（劣化コピーと割り切った設計です）。

## ジョブ定義の書き方

`jobs/` に `.md` ファイルを置くだけです。ファイルの中身全体が codex への
指示文になります。うまい定義は短く・1ジョブ1目的・受け入れ条件（テストで
確かめること）を明示すること。

**コミットはループに入れていません。** codex のサンドボックス（`-s
workspace-write`）は `.git` の書き込みをブロックするため・codex にコミット
させないのがこのキットの設計です。green を確認したら、人が中身をレビューして
から自分でコミットします（AI に書かせたものを無検査で git 歴史に載せない、
という安全側の型です）。

## 設定（config.json・任意）

```json
{
  "jobs_dir": "jobs",
  "codex_command": "codex exec --skip-git-repo-check -s workspace-write \"$(cat {job_file})\"",
  "test_command": "python3 -m pytest -q",
  "results_log": "results/log.jsonl",
  "stop_on_fail": true
}
```

- `codex_command`: 実行環境に合わせて差し替え可。`{job_file}` がジョブ定義の
  一時ファイルパスに置換されます。自動実行のオプションは Codex CLI の版で
  変わることがあるので、動かないときは `codex exec --help` で現行の
  サンドボックス指定を確認してください
- `test_command`: null にするとテスト自動実行を省けます
- `stop_on_fail`: false にすると失敗しても最後まで回して全記録を取ります

## 並列にしたくなったら

ドライバを複雑にする前に、まずは**コピーを増やす**のが安全です:
ジョブを別ディレクトリに分け（例 `jobs-a/` `jobs-b/`）、`config.json` も
別々にして、ターミナルを2つ開いてそれぞれ `run_loop.py` を走らせ、
**記録ログの書き込み先も分ける**。ここから先（共有キュー・競合制御・
失敗の自動復旧）は本格運用の領域で、このキットの範囲外です。

## 安全上の注意

- codex は作業ディレクトリ内で自由にファイルを書き換えます。必ず scratch
  ディレクトリで走らせ、成果物は**必ず自分の目でレビュー**してから使う
- ジョブ定義には秘密情報（APIキー・個人情報・社内URL）を書かない。
  定義ファイルはそのままプロセスに渡ります
- `results/log.jsonl` はローカルの実行記録です。共有前に中身を確認する

## ライセンス

Copyright (c) 2026 AI社員ラボ. All rights reserved.
本キットのコード・ドキュメントの著作権は作者に帰属します。
再配布・改変等のご利用は事前にご相談ください。
