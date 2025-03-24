# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 hwf1324 <1398969445@qq.com>

"""Automatically updates the mouse object vision Enhancement Provider."""

import mouseHandler
from autoSettingsUtils.autoSettings import SupportedSettingType
from autoSettingsUtils.driverSetting import BooleanDriverSetting
from vision import providerBase
from vision.visionHandlerExtensionPoints import EventExtensionPoints


class AutoUpdateMouseObjectSettings(providerBase.VisionEnhancementProviderSettings):
	coreCycle: bool

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
			BooleanDriverSetting(
				"coreCycle",
				# Translators: This label is the name of the setting that controls whether
				# the mouse object is automatically updated at the end of the core cycle.
				_("Automatically update the mouse object at the end of each core cycle"),
				defaultVal=True,
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

	def handleCoreCycle(self):
		if self._settings.coreCycle:
			mouseHandler.executeMouseMoveEvent(*mouseHandler.curMousePos)

	def terminate(self):
		pass

	def registerEventExtensionPoints(self, extensionPoints: EventExtensionPoints):
		extensionPoints.post_coreCycle.register(self.handleCoreCycle)


VisionEnhancementProvider = AutoUpdateMouseObjectProvider
