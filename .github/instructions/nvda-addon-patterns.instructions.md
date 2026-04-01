---
description: "NVDA アドオン開発パターン。Use when creating or modifying AppModule, GlobalPlugin, VisionEnhancementProvider, or overlay classes."
applyTo: "addon/**/*.py"
---
# NVDA アドオン開発パターン

## モジュール構成
- `addon/appModules/` — アプリ固有モジュール。クラス名は `AppModule`、`appModuleHandler.AppModule` を継承
- `addon/globalPlugins/` — グローバルプラグイン。クラス名は `GlobalPlugin`、`globalPluginHandler.GlobalPlugin` を継承
- `addon/visionEnhancementProviders/` — ビジョン強化プロバイダー。`providerBase.VisionEnhancementProvider` を継承

## AppModule パターン
```python
import appModuleHandler

class AppModule(appModuleHandler.AppModule):
	def event_mouseMove(self, obj, nextHandler, x: int, y: int):
		nextHandler()  # 必ず nextHandler() を呼ぶ
		# カスタム処理
```

## オーバーレイクラス
- `chooseNVDAObjectOverlayClasses` で条件に応じてクラスを差し込む
- IA2 属性の判定には `obj.IA2Attributes` を辞書比較で行う
- ウィンドウクラス名の判定には `winUser.getClassName()` を使う

## UIA 操作
- `UIAHandler.handler.MTAThreadQueue` を使って MTA スレッドで UIA クエリを実行する
- `mouseCacheRequest` 等のキャッシュリクエストは `UIAHandler.handler.baseCacheRequest.Clone()` で作成する
- `COMError` を必ず捕捉する

## 設定管理
- `config.conf` を使って NVDA の設定にアクセスする
- カスタム設定は `autoSettingsUtils` の `DriverSetting` / `NumericDriverSetting` を使用する
- GUI パネルは `SettingsPanel` + `AutoSettingsMixin` で実装する

## その他
- 対応 NVDA バージョン: 2022.1 以上（`addon_minimumNVDAVersion` で定義）
- Windows プラットフォーム前提（`ctypes.wintypes`, `winUser`, `winInputHook` 等を使用）
