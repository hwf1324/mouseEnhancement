# 鼠标增强

这是 NVDA 中使用鼠标增强功能的集合。
将来，某些功能可能会作为独立功能移出。

* 作者：hwf1324 <1398969445@qq.com>
* 兼容性：NVDA-2022.1 或更高版本

## 功能

* 修复 [Electron](https://www.electronjs.org/) 应用中的鼠标导航（仅 2024.4 或更高版本）。
  * Electron 应用，例如 [VS Code](https://code.visualstudio.com/)。
* 实验性修复 [WinUI](https://github.com/microsoft/microsoft-ui-xaml)、[Zoom](https://www.zoom.com/)、[飞书](https://www.feishu.cn/)应用中的鼠标导航，
  * [Windows 终端](https://github.com/microsoft/terminal)：如果文本识别单元室段落，则在终端控件中移动鼠标时，将文本识别单元限制为行。
* 修复部分 NVIDIA 控制面板中静态文本控件的错误描述。
* 修复了 [PDFgear](https://www.pdfgear.com/) 中按钮无法获取描述文本的问题。
* 在鼠标移动时报告 [Tree Style Tab](https://piro.sakura.ne.jp/xul/_treestyletab.html.en) 扩展上标签页的信息。
* 自动更新鼠标对象。当滚动鼠标滚轮或在 NVDA 核心周期的末尾时，自动更新鼠标对象。（这个功能在操作鼠标滚轮时可能非常有用。）可以在NVDA视觉设置面板中启用或禁用该功能。
  * 仅当在更新方式为“核心周期”时，鼠标移动事件延迟参数才会生效，以实现 <https://github.com/nvaccess/nvda/issues/19372>。

## 更新日志

### v0.9.1

* 使用 UIAHandler 的 MTA 线程进行 UIA 查询。

### v0.9.0

* 重构 Electron UIA 相关部分：
  * 使用 `IUIAutomation.ElementFromPointBuildCache` 方法从坐标获取 UIA 元素，用于创建重定向的鼠标对象。
  * 同时使用 `IUIAutomationCondition` 排除 `Name` 属性为空字符串的 UIA 元素，以修复鼠标导航 VS Code 时的一些问题。
    * 例如现在可以读取悬浮面板上的文本。
* 在仅限核心周期自动更新鼠标对象时添加鼠标移动事件延迟参数，作为 <https://github.com/nvaccess/nvda/issues/19372> 的实验性实现。
* 在鼠标移动时报告 Tree Style Tab 扩展上标签页的信息。

### v0.8.4

* 重构“强制使用应用程序的 UIA 实现”的判断逻辑，并排除 Chrome 浏览器侧边栏扩展对 Chrome 浏览器的影响。

### v0.8.3

* 禁用 `Intermediate D3D Window` 窗口类规则，因为 Chrome 也使用这个窗口类。

### v0.8.2

* 更新 Electron 规则以适配 UIA。

### v0.8.1

* 更新 PDFgear 规则。
* 更新插件模板。

### v0.8.0

* 移除不稳定的 Git for Windows 安装器相关功能。
* 更新插件模板。
* 添加乌克兰语的本地化和文档。

### v0.7.2

* 修复错误的 API 兼容版本，将 NVDA 支持的最低版本调整为 2022.1。

### v0.7.1

* 自动更新鼠标对象：增强了在滚动鼠标滚轮时自动更新鼠标对象的稳定性。
* 将 NVDA 鼠标挂钩接收到的鼠标消息转发到 `pre_handleWindowMessage` 扩展点。（不包括 wParam 和 lParam 参数，它们的将值设置为 `None`）

### v0.7.0

* 自动更新鼠标对象：新增了一种在滚动鼠标滚轮时自动更新鼠标对象的方法。
* 重构了“自动更新鼠标对象”的配置部分。
* 更新 NVDA 兼容性到 2025.1，并将 NVDA 支持的最低版本调整为 2021.1。
* 添加 zh_CN 翻译。

### v0.6.0

* 新增功能，可在NVDA核心周期结束时自动更新鼠标对象。

### v0.5.1

* Electron: 修复在 Chrome 地址栏浏览搜索建议时的冻结问题。
* 代码清理：应用 @josephsl 的建议。（代码注释尚未完善。）

### v0.5.0

* 实验性：在 Zoom、飞书中修复鼠标导航。
* Electron: 将重定向对象限制为 IAccessible，以排除使用 UIA 的应用程序。
* Git for Windows安装程序：捕获可以安全忽略的异常。

### v0.4.0

* 实验性：通过在遇到具有特定 `windowClassName` 属性的对象时使 `obj.appModule.isGoodUIAWindow` 始终返回 `True`，来修复 WinUI 应用程序中的鼠标导航问题。
  * Windows 终端：如果文本识别单元室段落，则在终端控件中移动鼠标时，将文本识别单元限制为行。
* Electron: 清理了一些不必要的判断逻辑。
* 更新插件模板。

### v0.3.0

* 将插件的名称更改为：Mouse Enhancement。（未考虑更新插件的情况。）
* 在安全界面时忽略错误，因为该对象没有 `windowClassName` 属性。
* 鼠标导航可以报告 Git for Windows 安装程序中选项的描述。(无法单独查看各个选项。)
* 更新插件模板。

### v0.2.0

* 修复部分 NVIDIA 控制面板中静态文本控件的错误描述。
* 修复了 PDFgear 中按钮无法获取描述文本的问题。

### v0.1.0

* 修复 Electron 应用程序中的鼠标导航。

## 致谢

* 感谢 @jcsteh 在 <https://github.com/nvaccess/nvda/issues/17108> 中的指导，帮助修复了 Electron 中的鼠标导航问题。
* Thanks to @codeofdusk in <https://github.com/nvaccess/nvda/issues/17407#issuecomment-2544712156> for the way to experimentally fix mouse tracking in WinUI apps.
* 感谢 @codeofdusk 在 <https://github.com/nvaccess/nvda/issues/17407#issuecomment-2544712156> 上提供了用于实验性修复 WinUI 应用程序中鼠标导航问题的方法。
