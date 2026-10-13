# PyPI 公開手順 (openmcpart)

このドキュメントは `openmcpart` を PyPI へ公開するための手順です。
推奨は **GitHub Actions + Trusted Publishing** で、APIトークンをリポジトリや Secrets に置かずに公開できます。

- 配布名: `openmcpart`(PyPI上で未取得であることは確認済み)
- バージョンの単一情報源: `src/openmcpart/__init__.py` の `__version__`
- ビルドバックエンド: hatchling(`pyproject.toml`)

---

## 0. 事前確認(ローカル)

```bash
python -m build            # dist/ に sdist と wheel を生成
python -m twine check --strict dist/*
```

ビルド済みwheelの動作確認:

```bash
python -m venv /tmp/verify && /tmp/verify/bin/pip install dist/*.whl
/tmp/verify/bin/openmcpart --help
/tmp/verify/bin/openmcpart audit . --fail-on high
```

メタデータの要件(重要):

- `license = "MIT"` + `license-files = ["LICENSE"]`(PEP 639)。書き出されるメタデータは `License-Expression: MIT` / `License-File: LICENSE`。
- **`License :: OSI Approved :: MIT License` のようなライセンスclassifierは併記しないこと。** `License-Expression` がある状態でライセンスclassifierを併記すると PyPI はアップロードを拒否します(PEP 639)。
- `Metadata-Version` は 2.4 以上が必要(`License-Expression` / `License-File` を使うため)。hatchling は自動的に 2.5 を出力します。

---

## 1. PyPI アカウントと 2FA

1. https://pypi.org/account/register/ でアカウントを作成
2. 2FA(WebAuthn 推奨)を有効化 — 未設定だと新規プロジェクトの公開ができません

## 2. Trusted Publisher を登録(Pending Publisher)

プロジェクトがまだPyPIに存在しないため、「保留中のパブリッシャー」として先に登録します。

1. https://pypi.org/manage/account/publishing/ を開く
2. 「Add a new pending publisher」で以下を入力

| 項目 | 値 |
| --- | --- |
| PyPI Project Name | `openmcpart` |
| Owner | `hrfrutrd-dev` |
| Repository name | `openmcpart` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

3. 保存

TestPyPI でも予行演習する場合は https://test.pypi.org/manage/account/publishing/ に同じ内容で登録します(Environment name は `testpypi`)。

## 3. 予行演習(任意・推奨): TestPyPI へ公開

1. GitHub の Actions タブ → **Publish to PyPI** → **Run workflow**
2. `repository` で `testpypi` を選択して実行
3. 成功したら確認(依存の `mcp` はTestPyPIに無いため `--no-deps` を付けます)

```bash
pip install --index-url https://test.pypi.org/simple/ --no-deps openmcpart
```

## 4. 本番: PyPI へ公開

Trusted Publishing では **GitHub Release の公開がトリガー**です。

1. バージョンを更新する(例: `0.3.0` → `0.3.1`)
   - `src/openmcpart/__init__.py` の `__version__` を書き換える(ここが唯一の定義箇所)
   - 変更を `main` にマージ
2. GitHub で Release を作成
   - Tag: `v0.3.1`(先頭の `v` は任意。ワークフローが `v` を除いて照合します)
   - Target: `main`
3. Release を **Publish** すると `publish.yml` が起動し、以下を実行します
   - タグと `__version__` の一致確認
   - sdist / wheel のビルドと `twine check --strict`
   - クリーンなvenvでのwheelインストールとCLI動作確認
   - PyPI へのアップロード(OIDC、トークン不要)
4. https://pypi.org/project/openmcpart/ で反映を確認

> 補足: Actions タブから `workflow_dispatch` で `pypi` を選んでも公開できますが、通常は Release 経由を推奨します。

---

## 代替手段: API トークンで手動アップロード

CI を使わない場合の手順です。

1. https://pypi.org/manage/account/token/ でトークンを作成
   - スコープ: 「Project: openmcpart」(初回公開時は PyPI にプロジェクトが無いため、初回のみ Account スコープのトークンが必要)
2. アップロード

```bash
python -m build
python -m twine upload dist/*
# ユーザー名: __token__   パスワード: pypi-... のトークン
```

環境変数を使う場合:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-xxxxxxxx
python -m twine upload dist/*
```

トークンはリポジトリにコミットしないでください(`.env` は `.gitignore` 済み)。

---

## バージョン更新とリリース手順(まとめ)

```bash
# 1. バージョン更新(単一情報源)
#    src/openmcpart/__init__.py: __version__ = "0.3.1"

# 2. 検証
python -m pytest -q
ruff check src tests
python -m build && python -m twine check --strict dist/*

# 3. コミット & プッシュ後、GitHub Release を v0.3.1 で作成
```

---

## トラブルシューティング

| 症状 | 原因と対処 |
| --- | --- |
| `400 License classifiers are deprecated / not allowed` | `License-Expression` とライセンスclassifierの併記。classifierを削除する |
| `license-file introduced in metadata version 2.4, not 2.x` | 古いビルドツール。`hatchling` を最新にして再ビルドする |
| `File already exists` | 同一バージョンは上書き不可。`__version__` を上げる |
| `403 Invalid or non-existent authentication information` | トークンのスコープ/値の誤り。または OIDC 設定(Workflow name / Environment 名)の不一致 |
| GitHub Release でワークフローが起動しない | `.github/workflows/publish.yml` が `main` に存在するか、Release が「published」になっているかを確認 |
| 名前が既に使われている | PyPI は名前の再利用を認めません。`pyproject.toml` の `name` を変更する |

## 参考リンク

- Trusted Publishing: https://docs.pypi.org/trusted-publishers/
- パッケージング仕様: https://packaging.python.org/en/latest/specifications/core-metadata/
- PEP 639(ライセンスメタデータ): https://peps.python.org/pep-0639/
