# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 hwf1324 <1398969445@qq.com>

"""Automatically updates the mouse object vision Enhancement Provider."""

import addonHandler
import core
import mouseHandler
import winInputHook
import wx
from autoSettingsUtils.autoSettings import SupportedSettingType
from autoSettingsUtils.driverSetting import DriverSetting, NumericDriverSetting
from autoSettingsUtils.utils import StringParameterInfo
from gui import guiHelper, nvdaControls
from gui.settingsDialogs import (
	AutoSettingsMixin,
	DriverSettingChanger,
	SettingsPanel,
	VisionProviderStateControl,
)
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
	mouseMoveEventDelay: int

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
				_("Automatic update mouse object method"),
				defaultVal="mouseWheel",
			),
			NumericDriverSetting(
				"mouseMoveEventDelay",
				# Translators: This label is the name of the setting that controls the mouse move event delay.
				_("Mouse move event delay (%S)"),
				defaultVal=0,
				minVal=0,
				maxVal=1000,
				minStep=100,
				normalStep=100,
				largeStep=1000,
			),
		]

	def _get_supportedSettings(self) -> SupportedSettingType:
		return self.getPreInitSettings()


class SpinDriverSettingChanger(DriverSettingChanger):
	def __call__(self, evt: wx.SpinEvent):
		evt.Skip()  # allow other handlers to also process this event.
		val = evt.GetPosition()
		setattr(self.driver, self.setting.id, val)


class AutoUpdateMouseObjectSettingsPanel(
	AutoSettingsMixin,
	SettingsPanel,
):
	def __init__(
		self,
		parent: wx.Window,
		providerControl: VisionProviderStateControl,
	):
		self._providerControl = providerControl
		super().__init__(parent)

	def _buildGui(self) -> None:
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)

		self._enabledCheckbox = wx.CheckBox(
			self,
			# Translators: Enable checkbox on a vision enhancement provider on the vision settings category panel
			label=_("Enable Auto Update Mouse Object"),
		)

		self.mainSizer.Add(self._enabledCheckbox)
		self.mainSizer.AddSpacer(size=self.scaleSize(10))
		# this options separator is done with text rather than a group box because a groupbox is too verbose,
		# but visually some separation is helpful, since the rest of the options are really sub-settings.
		self.optionsText = wx.StaticText(
			self,
			# Translators: Options label on a vision enhancement provider on the vision settings category panel
			label=_("Options:"),
		)
		self.mainSizer.Add(self.optionsText)

		self.lastControl = self.optionsText
		self.settingsSizer = wx.BoxSizer(wx.VERTICAL)
		self.makeSettings(self.settingsSizer)
		self.mainSizer.Add(self.settingsSizer, border=self.scaleSize(15), flag=wx.LEFT | wx.EXPAND)
		self.mainSizer.Fit(self)
		self.SetSizer(self.mainSizer)

	def getSettings(self) -> AutoUpdateMouseObjectSettings:
		# AutoSettingsMixin uses the getSettings method (via getSettingsStorage) to get the instance which is
		# used to get / set attributes. The attributes must match the id's of the settings.
		# We want them set on our settings instance.
		return VisionEnhancementProvider.getSettings()

	def makeSettings(self, sizer: wx.BoxSizer) -> None:
		settingsInst = self.getSettings()
		settingsStorage = self._getSettingsStorage()
		# for setting in settingsInst.supportedSettings:
		# 	if setting.id == "mouseMoveEventDelay":
		# 		mouseDelaySetting: NumericDriverSetting = setting
		# if not mouseDelaySetting:
		# 	raise LookupError

		# self.updateDriverSettings(mouseDelaySetting.id)
		# sSpin = self._makeSppinSettingControl(mouseDelaySetting, settingsStorage)
		# self.sizerDict[mouseDelaySetting.id] = sSpin
		# sizer.Insert(
		# 	len(self.sizerDict) - 1,
		# 	sSpin,
		# 	border=10,
		# 	flag=wx.BOTTOM,
		# )
		self.updateDriverSettings()

	def onPanelActivated(self) -> None:
		self.lastControl = self.optionsText

	def _makeSppinSettingControl(
		self,
		setting: NumericDriverSetting,
		settingsStorage,
	) -> wx.BoxSizer:
		"""Constructs appropriate GUI controls for given L{DriverSetting} such as label and spin.
		@param setting: Setting to construct controls for
		@param settingsStorage: where to get initial values / set values.
			This param must have an attribute with a name matching setting.id.
			In most cases it will be of type L{AutoSettings}
		@return: wx.BoxSizer containing newly created controls.
		"""
		labeledControl = guiHelper.LabeledControlHelper(
			self,
			f"{setting.displayNameWithAccelerator}:",
			nvdaControls.SelectOnFocusSpinCtrl,
			minValue=setting.minVal,
			maxValue=setting.maxVal,
		)
		lSpin = labeledControl.control
		setattr(self, f"{setting.id}Spin", lSpin)
		lSpin.Bind(
			wx.EVT_SPINCTRL,
			SpinDriverSettingChanger(
				settingsStorage,
				setting,
			),
		)
		self.bindHelpEvent(
			self._getSettingControlHelpId(setting.id),
			lSpin,
		)
		lSpin.SetValue(getattr(settingsStorage, setting.id))
		if self.lastControl:
			lSpin.MoveAfterInTabOrder(self.lastControl)
		self.lastControl = lSpin
		return labeledControl.sizer


class AutoUpdateMouseObjectProvider(providerBase.VisionEnhancementProvider):
	_settings = AutoUpdateMouseObjectSettings()

	@classmethod
	def canStart(cls):
		return True

	@classmethod
	def getSettings(cls) -> AutoUpdateMouseObjectSettings:
		return cls._settings

	# @classmethod
	# def getSettingsPanelClass(cls) -> type[AutoUpdateMouseObjectSettingsPanel]:
	# 	return AutoUpdateMouseObjectSettingsPanel

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
