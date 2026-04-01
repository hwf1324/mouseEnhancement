---
description: "ビルド・リリース手順。Use when building the addon, updating version numbers, creating releases, or modifying sconstruct/buildVars."
applyTo: ["buildVars.py", "sconstruct", "manifest*.tpl", ".github/workflows/**"]
---
# ビルド・リリース手順

## ビルドシステム
- **SCons** を使用（`sconstruct` がエントリポイント）
- Python 3.10 以上が必要（推奨: 3.11 以上）

## ビルドコマンド
```shell
# アドオンをビルド
scons

# 開発ビルド（タイムスタンプ版）
scons version=YYYYMMDD.0.0

# ポットファイルの生成
scons pot
```

## バージョン管理
- バージョンは `buildVars.py` の `addon_version` で定義する
- `major.minor.patch` 形式（すべて整数）で NV Access アドオンストアに準拠する
- 開発ビルドでは `scons version=` で上書き可能

## リリース時のチェックリスト
1. `buildVars.py` の `addon_version` を更新する
2. `addon_changelog` に変更内容を記述する（`_()` でラップ）
3. `addon_lastTestedNVDAVersion` を最新テスト済みバージョンに更新する
4. `changelog.md` を更新する
5. 各ロケールの `readme.md` を更新する
6. `scons` でビルドし `.nvda-addon` ファイルを生成する

## マニフェスト
- `manifest.ini.tpl` と `manifest-translated.ini.tpl` がテンプレート
- ビルド時に `buildVars.py` の値で自動生成される

## CI/CD
- `.github/workflows/build_addon.yml` で自動ビルドが設定されている
- Dependabot（`.github/dependabot.yml`）で依存関係を自動更新
