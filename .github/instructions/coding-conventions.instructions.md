---
description: "Python コーディング規約。Use when writing or modifying Python files, reviewing code style, or fixing lint errors."
applyTo: "**/*.py"
---
# コーディング規約

## インデント・フォーマット
- インデントは**タブ文字**を使用する（スペース不可）
- 行長の上限は **110文字**（Ruff 設定に準拠）

## 命名規則
- クラス名: `CamelCase`（例: `RedirectChromiumUIA`, `AppModule`）
- 関数・変数: `snake_case`（例: `mouse_move_event_delay`）
- 定数: `UPPER_SNAKE_CASE`（例: `WM_MOUSEWHEEL`, `ELECTRON_IA2_ATTRIBUTES`）

## 型注釈
- Pyright strict モードに準拠する
- メソッドのパラメータと戻り値に型注釈を付ける
- `from __future__ import annotations` は使わず、Python 3.10+ のネイティブ型構文を使用する
  - `list[str]`、`dict[str, int]`、`X | None` など

## ファイルヘッダー
すべての Python ファイルに以下のライセンスヘッダーを付ける:

```python
# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) <年> hwf1324 <1398969445@qq.com>
```

## リンター・フォーマッター
- **Ruff** でリントとフォーマットを行う
- `W191`（タブインデント警告）は無視される設定済み
- `sconstruct` では `F821`（未定義名）を無視する

## その他
- デバッグ用フラグは `isDebug: bool = False` で定義する
- `from logHandler import log` を使ってログを出力する
