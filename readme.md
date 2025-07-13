# Mouse Enhancement

This is a collection of enhancements for mouse usage in NVDA.
Some features may be moved out as standalone features in the future.

* Author: hwf1324 <1398969445@qq.com>
* Compatibility: NVDA-2021.1 or later

## Features

* Fix mouse tracking in [Electron](https://www.electronjs.org/) apps (Only 2024.4 or later).
  * Electron apps, such as [VS Code](https://code.visualstudio.com/).
* Experimental fix mouse tracking in [WinUI](https://github.com/microsoft/microsoft-ui-xaml), [Zoom](https://www.zoom.com/), [飞书](https://www.feishu.cn/) apps.
  * [Windows Terminal](https://github.com/microsoft/terminal): If the text unit is a paragraph, moving the mouse in the Terminal control restricts the text unit to lines.
* Fix a part of the NVIDIA Control Panel where the content of the static text description control is incorrect.
* Fixed the problem that some buttons in [PDFgear](https://www.pdfgear.com/) could not get the description text.
* Mouse tracking can report the description of the option in the [Git for Windows](https://git-scm.com/downloads/win) installer. (Individual options cannot be viewed individually.)
* Auto Update Mouse Object. Automatically update the mouse object when scrolling the mouse wheel or at the end of each NVDA core cycle. (This feature may be useful when using the mouse wheel.) This can be enabled/disabled in the NVDA vision settings panel.

## Changelog

### v0.7.0

* Auto Update Mouse Object: Added a way to automatically update the mouse object when scrolling the mouse wheel.
* Reconstructed the configuration section of Auto Update Mouse Object.
* Updated NVDA compatibility to 2025.1 and adjusted minimum NVDA support version to 2021.1.
* Add zh_CN translation.

### v0.6.0

* Added the ability to automatically update the mouse object at the end of each NVDA core cycle.

### v0.5.1

* Electron: Fix freeze when browsing search suggestions in Chrome's address bar.
* Code cleanup: applying @josephsl's suggestions. (Code comment not perfected.)

### v0.5.0

* Experimental: Fix mouse tracking in Zoom, 飞书.
* Electron: Restrict the redirection object to IAccessible to exclude applications that use UIA.
* Git for Windows installer: Catch exceptions that can be safely ignored.

### v0.4.0

* Experimental: Fix mouse tracking in WinUI apps by making `obj.appModule.isGoodUIAWindow` always return `True` when an object with a specific `windowClassName` property is encountered.
  * Windows Terminal: If the text unit is a paragraph, moving the mouse in the Terminal control restricts the text unit to lines.
* Electron: cleaned up some unnecessary judgment logic.
* Update add-on template.

### v0.3.0

* Change the add-on name to: Mouse Enhancement. (Doesn't take into account add-on upgrades.)
* Ignore the error when entering the security screen because the object does not have the windowClassName attribute.
* Mouse tracking can report the description of the option in the Git for Windows installer. (Individual options cannot be viewed individually.)
* Update add-on template.

### v0.2.0

* Fix a part of the NVIDIA Control Panel where the content of the static text description control is incorrect.
* Fixed the problem that some buttons in PDFgear could not get the description text.

### v0.1.0

* Fix mouse tracking in Electron apps.

## Acknowledgements

* Thanks to @jcsteh in <https://github.com/nvaccess/nvda/issues/17108> for his guidance in fixing mouse tracking in the Electron app.
* Thanks to @codeofdusk in <https://github.com/nvaccess/nvda/issues/17407#issuecomment-2544712156> for the way to experimentally fix mouse tracking in WinUI apps.
