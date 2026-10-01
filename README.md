# codex-loop-starter

AI に「実装 → テスト → 記録」を丸ごとやらせる最小の仕組みです。無料で・
そのまま使えます。

## 1行で試す（macOS / Linux）

ターミナルを開いて、この1行をコピーして貼り付けて実行してください。

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/jinno2/codex-loop-starter/main/start.sh)"
```

数分待つと、こうなります:

- `try-loop/` フォルダができて、codex がサンプル（文字計数ツール）を実装します
- テストが自動で走って、結果が `try-loop/results/log.jsonl` に記録されます
- できたものは `try-loop/counter.py` — 見て確かめたらフォルダごと削除して大丈夫です

## 必要なもの（2つだけ）

- [Codex CLI](https://github.com/openai/codex) が入っていて認証済み（`codex login` 済み）
- python3（macOS ならだいたい入っています）

Windows の場合は WSL か Git Bash から上のコマンドを実行してください。

## 安心のための説明

この1行は・このリポジトリにある `start.sh` をダウンロードして実行します。
`start.sh` が作るのは `try-loop/` フォルダだけで・**あなたのPCの他のファイルには
触れません**。AI が書いたものは**必ず自分の目で確認してから**使ってください。

## 詳細を見たい方はこちら

カスタマイズの方法・仕組みの詳細・ジョブ定義の書き方は engineer ブランチ:
https://github.com/jinno2/codex-loop-starter/tree/engineer

## ライセンス

Copyright (c) 2026 AI社員ラボ. All rights reserved.
本キットのコード・ドキュメントの著作権は作者に帰属します。
再配布・改変等のご利用は事前にご相談ください。
