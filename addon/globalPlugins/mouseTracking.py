# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2024-2025 hwf1324 <1398969445@qq.com>

from ctypes.wintypes import POINT

import controlTypes
import globalPluginHandler
import IAccessibleHandler
import UIAHandler
import winUser
from comtypes import COMError
from logHandler import log
from NVDAObjects import NVDAObject
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible.chromium import Document
from NVDAObjects.IAccessible.ia2Web import Ia2Web
from NVDAObjects.UIA import UIA


isDebug: bool = False

ELECTRON_IA2_ATTRIBUTES = {"class": "View"}
CHROME_SIDEBAR_EXTENSION_IA2_ATTRIBUTES = {"class": "SidePanel::BorderView"}


class RedirectDocument(Ia2Web):

	def objectFromPointRedirect(self, x: int, y: int):
		docObj: Document = self.previous.lastChild
		try:
			redirect = docObj.IAccessibleObject.accHitTest(x, y)
		except COMError:
			return None

		if not redirect:
			return None

		redirect = IAccessibleHandler.normalizeIAccessible(redirect)
		obj: IAccessible = IAccessible(IAccessibleObject=redirect, IAccessibleChildID=winUser.CHILDID_SELF)

		return obj


class RedirectChromiumUIA(Ia2Web):
	def objectFromPointRedirect(self, x: int, y: int):
		emptyNamePropertyCondition = UIAHandler.handler.clientObject.CreateNotCondition(
			UIAHandler.handler.clientObject.CreatePropertyCondition(
				UIAHandler.UIA.UIA_NamePropertyId,
				"",
			)
		)
		mouseCacheRequest = UIAHandler.handler.baseCacheRequest.Clone()
		mouseCacheRequest.TreeFilter = UIAHandler.handler.clientObject.CreateAndConditionFromArray(
			[
				# UIAHandler.handler.clientObject.CreateNotCondition(
				# 	UIAHandler.handler.clientObject.CreatePropertyCondition(
				# 		UIAHandler.UIA.UIA_ControlTypePropertyId,
				# 		UIAHandler.UIA_GroupControlTypeId,
				# 	),
				# ),
				emptyNamePropertyCondition,
			]
		)
		try:
			redirect = UIAHandler.handler.clientObject.ElementFromPointBuildCache(
				POINT(x, y), mouseCacheRequest
			)
		except COMError:
			return None
		if not redirect:
			return None
		obj = UIA(UIAElement=redirect)
		return obj


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def chooseNVDAObjectOverlayClasses(self, obj: NVDAObject, clsList: list[type[NVDAObject]]):
		try:
			if obj.role == controlTypes.Role.PANE:
				if (  # Electron
					isinstance(obj, IAccessible)
					and obj.IA2Attributes in (
						ELECTRON_IA2_ATTRIBUTES,
						CHROME_SIDEBAR_EXTENSION_IA2_ATTRIBUTES,  # Chrome's Sidebar
					)
					and winUser.getClassName(obj.IA2WindowHandle) == "Chrome_WidgetWin_1"
				):
					if (
						obj.previous.lastChild.windowClassName == "Chrome_RenderWidgetHostHWND"
					):
						clsList.insert(0, RedirectDocument)
					elif (
						isinstance(obj.parent, UIA)
						and obj.childCount == 0
					):
						clsList.insert(0, RedirectChromiumUIA)
				if isDebug:
					log.debug("Redirecting the devInfo of the object:\n%s" % "\n".join(obj.devInfo))

				if (  # Force the use of the application's UIA implementation
					obj.windowClassName in (
						"Microsoft.UI.Content.DesktopChildSiteBridge",  # WinUI
						"Windows.UI.Composition.DesktopWindowContentBridge",
						# ! Since #18 temporarily disables this rule, note: Chrome also uses this window class instead of just Electron.
						# "Intermediate D3D Window",  # Chromium with UIA
					)
				) and not obj.appModule.isGoodUIAWindow(obj.windowHandle):
					log.info(
						"Determines the devInfo that is forced to be a good UIA window object:\n%s"
						% "\n".join(obj.devInfo)
					)
					obj.appModule.isGoodUIAWindow = lambda hwnd: True
		except AttributeError:
			pass
