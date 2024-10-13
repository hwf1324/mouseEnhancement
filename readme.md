# Mouse Enhancement

This is a collection of enhancements for mouse usage in NVDA.
Some features may be moved out as standalone features in the future.

* Author: hwf1324 <1398969445@qq.com>
* Compatibility: NVDA-2024.4 or later

## Features

* Fix mouse tracking in [Electron](https://www.electronjs.org/) apps.
  * Electron apps, such as [VS Code](https://code.visualstudio.com/).
* Fix a part of the NVIDIA Control Panel where the content of the static text description control is incorrect.
* Fixed the problem that some buttons in [PDFgear](https://www.pdfgear.com/) could not get the description text.
* Mouse tracking can report the description of the option in the [Git for Windows](https://git-scm.com/downloads/win) installer. (Individual options cannot be viewed individually.)


## Usage

To enable these features, you need to install the mouseEnhancements add-on from the Add-ons Store. After installing, restart NVDA.

## Known issues

None.

## Changelog

### 0.3.0

* Change the add-on name to: Mouse Enhancement. (Doesn't take into account add-on upgrades.)
* Ignore the error when entering the security screen because the object does not have the windowClassName attribute.
* Mouse tracking can report the description of the option in the Git for Windows installer. (Individual options cannot be viewed individually.)

### 0.2.0

* Fix a part of the NVIDIA Control Panel where the content of the static text description control is incorrect.
* Fixed the problem that some buttons in PDFgear could not get the description text.

### 0.1.0

* Fix mouse tracking in Electron apps.

## Acknowledgements

Thanks to @jcsteh for his guidance in fixing mouse tracking in the Electron app.
