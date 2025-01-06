# Mouse Enhancement

This is a collection of enhancements for mouse usage in NVDA.
Some features may be moved out as standalone features in the future.

* Author: hwf1324 <1398969445@qq.com>
* Compatibility: NVDA-2024.4 or later

## Features

* Fix mouse tracking in [Electron](https://www.electronjs.org/) apps (2024.4 only).
  * Electron apps, such as [VS Code](https://code.visualstudio.com/).
* Experimental fix mouse tracking in [WinUI](https://github.com/microsoft/microsoft-ui-xaml) apps.
  * [Windows Terminal](https://github.com/microsoft/terminal): If the text unit is a paragraph, moving the mouse in the Terminal control restricts the text unit to lines.
* Fix a part of the NVIDIA Control Panel where the content of the static text description control is incorrect.
* Fixed the problem that some buttons in [PDFgear](https://www.pdfgear.com/) could not get the description text.
* Mouse tracking can report the description of the option in the [Git for Windows](https://git-scm.com/downloads/win) installer. (Individual options cannot be viewed individually.)

## Changelog

### 0.4.0

* Experimental: Fix mouse tracking in WinUI apps by making `obj.appModule.isGoodUIAWindow` always return `True` when an object with a specific `windowClassName` property is encountered.
  * Windows Terminal: If the text unit is a paragraph, moving the mouse in the Terminal control restricts the text unit to lines.
* Electron: cleaned up some unnecessary judgment logic.
* Update add-on template.

### 0.3.0

* Change the add-on name to: Mouse Enhancement. (Doesn't take into account add-on upgrades.)
* Ignore the error when entering the security screen because the object does not have the windowClassName attribute.
* Mouse tracking can report the description of the option in the Git for Windows installer. (Individual options cannot be viewed individually.)
* Update add-on template.

### 0.2.0

* Fix a part of the NVIDIA Control Panel where the content of the static text description control is incorrect.
* Fixed the problem that some buttons in PDFgear could not get the description text.

### 0.1.0

* Fix mouse tracking in Electron apps.

## Acknowledgements

Thanks to @jcsteh in https://github.com/nvaccess/nvda/issues/17108 for his guidance in fixing mouse tracking in the Electron app.
Thanks to @codeofdusk in https://github.com/nvaccess/nvda/issues/17407#issuecomment-2544712156 for the way to experimentally fix mouse tracking in WinUI apps.
