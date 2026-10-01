# codex-loop-starter（1行スターター版）

AI に「実装 → テスト → 記録」を丸ごとやらせる最小の仕組みを、
**コマンド1行**で手元で試せるようにしたキットです（macOS / Linux）。

## 1行で試す

ターミナルを開いて、この1行をコピーして貼り付けて実行してください。

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/jinno2/codex-loop-starter/one-liner/start.sh)"
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
`start.sh` がやることは以下だけで・**あなたのPCの他のファイルには触れません**:

1. codex と python3 の確認（無ければ日本語で案内して止まります）
2. `try-loop/` フォルダを作る
3. ドライバ（`run_loop.py`）とサンプルジョブをダウンロードする
4. codex にサンプル実装をさせて・テストを走らせ・記録する

AI が書いたものは**必ず自分の目で確認してから**使ってください。このキットは
コードを git にコミットさせません — 人が確認してから自分でコミットするのが
安全側の型です。

## さらに自分の仕事をやらせたい

`try-loop/jobs/` に指示文の `.md` ファイルを足して、もう1回 `python3 run_loop.py`
を実行するだけです。書き方のくふうは main ブランチの README を参照:

https://github.com/jinno2/codex-loop-starter（エンジニア向け・カスタマイズ全般）

## ライセンス

Copyright (c) 2026 AI社員ラボ. All rights reserved.
本キットのコード・ドキュメントの著作権は作者に帰属します。
再配布・改変等のご利用は事前にご相談ください。
