# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 hwf1324 <1398969445@qq.com>

"""Automatically updates the mouse object vision Enhancement Provider."""

import addonHandler
import core
import mouseHandler
import winInputHook
from autoSettingsUtils.autoSettings import SupportedSettingType
from autoSettingsUtils.driverSetting import DriverSetting
from autoSettingsUtils.utils import StringParameterInfo
from logHandler import log
from vision import providerBase
from vision.visionHandlerExtensionPoints import EventExtensionPoints
from winAPI.messageWindow import pre_handleWindowMessage


addonHandler.initTranslation()

WM_MOUSEHWHEEL = 0x020E
WM_MOUSEWHEEL = 0x020A

old_mouseCallback = mouseHandler.internal_mouseEvent


def forwardHookMouseMessage(msg: int, x: int, y: int, injected: int):
	pre_handleWindowMessage.notify(msg=msg, wParam=None, lParam=None)

	return old_mouseCallback(msg, x, y, injected)


class AutoUpdateMouseObjectSettings(providerBase.VisionEnhancementProviderSettings):
	updateMethod: str

	availableUpdatemethods = {
		# Translators: This label is the name of the setting that controls whether
		# the mouse object is automatically updated when the mouse wheel is scrolled.
		"mouseWheel": StringParameterInfo("mouseWheel", _("Mouse Wheel")),
		# Translators: This label is the name of the setting that controls whether
		# the mouse object is automatically updated at the end of the core cycle.
		"coreCycle": StringParameterInfo("coreCycle", _("Core Cycle")),
	}

	@classmethod
	def getId(cls) -> str:
		return "autoUpdateMouseObject"

	@classmethod
	def getDisplayName(cls) -> str:
		# Translators: This label is the display name of the Auto update mouse object vision Enhancement Provider.
		return _("Auto Update Mouse Object")

	@classmethod
	def getPreInitSettings(cls) -> SupportedSettingType:
		return [
			DriverSetting(
				"updateMethod",
				# Translators: This label is the name of the setting that controls
				# the automatic update method for the mouse object.
				_("Automatic update mouse object method:"),
				defaultVal="mouseWheel",
			),
		]

	def _get_supportedSettings(self) -> SupportedSettingType:
		settings = []

		settings.extend(self.getPreInitSettings())

		return settings


class AutoUpdateMouseObjectProvider(providerBase.VisionEnhancementProvider):
	_settings = AutoUpdateMouseObjectSettings()

	@classmethod
	def canStart(cls):
		return True

	@classmethod
	def getSettings(cls) -> AutoUpdateMouseObjectSettings:
		return cls._settings

	def __init__(self):
		super().__init__()
		if winInputHook.mouseCallback:
			log.info("Hooking mouseHandler.internal_mouseEvent function...")
			winInputHook.setCallbacks(mouse=forwardHookMouseMessage)
			pre_handleWindowMessage.register(self.handleWindowMouseWheelMessage)

	def handleWindowMouseWheelMessage(self, msg: int, wParam: int, lParam: int):
		if self._settings.updateMethod == "mouseWheel" and msg in (WM_MOUSEWHEEL, WM_MOUSEHWHEEL):
			core.callLater(100, mouseHandler.executeMouseMoveEvent, *mouseHandler.curMousePos)

	def handleCoreCycle(self):
		if self._settings.updateMethod == "coreCycle":
			mouseHandler.executeMouseMoveEvent(*mouseHandler.curMousePos)

	def terminate(self):
		pre_handleWindowMessage.unregister(self.handleWindowMouseWheelMessage)
		if winInputHook.mouseCallback:
			log.info("Unhooking mouseHandler.internal_mouseEvent function...")
			winInputHook.setCallbacks(mouse=old_mouseCallback)

	def registerEventExtensionPoints(self, extensionPoints: EventExtensionPoints):
		extensionPoints.post_coreCycle.register(self.handleCoreCycle)


VisionEnhancementProvider = AutoUpdateMouseObjectProvider
