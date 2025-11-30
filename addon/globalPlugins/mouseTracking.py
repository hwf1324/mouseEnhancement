# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2024-2025 hwf1324 <1398969445@qq.com>

import controlTypes
import globalPluginHandler
import IAccessibleHandler
import winUser
from logHandler import log
from NVDAObjects import NVDAObject
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible.chromium import Document
from NVDAObjects.IAccessible.ia2Web import Ia2Web
from NVDAObjects.UIA import UIA


isDebug: bool = False

ELECTRON_IA2_ATTRIBUTES = {"class": "View"}
CHROME_SIDEBAR_EXTENSION_IA2_ATTRIBUTES = {"class": "BorderView"}


class RedirectDocument(Ia2Web):

	def objectFromPointRedirect(self, x: int, y: int):
		docObj: Document = self.previous.lastChild
		redirect = docObj.IAccessibleObject.accHitTest(x, y)

		if not redirect:
			return None

		redirect = IAccessibleHandler.normalizeIAccessible(redirect)
		obj: IAccessible = IAccessible(IAccessibleObject=redirect, IAccessibleChildID=winUser.CHILDID_SELF)

		return obj


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def chooseNVDAObjectOverlayClasses(self, obj: NVDAObject, clsList: list[type[NVDAObject]]):
		try:
			if obj.role == controlTypes.Role.PANE:
				if (  # Electron
					isinstance(obj, IAccessible)  # TODO: The UIA situation needs to be investigated.
					and obj.IA2Attributes in (
						ELECTRON_IA2_ATTRIBUTES,
						CHROME_SIDEBAR_EXTENSION_IA2_ATTRIBUTES,  # Chrome's Sidebar
					)
					and winUser.getClassName(obj.IA2WindowHandle) == "Chrome_WidgetWin_1"
					and obj.previous.lastChild.windowClassName == "Chrome_RenderWidgetHostHWND"
				):
					if isDebug:
						log.debug("Redirecting the devInfo of the document object:\n%s" % "\n".join(obj.devInfo))
					clsList.insert(0, RedirectDocument)

				if (  # Force the use of the application's UIA implementation
					obj.windowClassName in (
						"Microsoft.UI.Content.DesktopChildSiteBridge",  # WinUI
						"Windows.UI.Composition.DesktopWindowContentBridge",
						# ! Since #18 temporarily disables this rule, note: Chrome also uses this window class instead of just Electron.
						# "Intermediate D3D Window",  # Chromium with UIA
					) or (  # TODO: Rules may not be tight enough
						isinstance(obj, IAccessible)
						and obj.IA2Attributes in (
							CHROME_SIDEBAR_EXTENSION_IA2_ATTRIBUTES,  # Ignores Chrome's Sidebar
						)
						and obj.childCount == 0
						and isinstance(obj.parent, UIA)
					)
				) and not obj.appModule.isGoodUIAWindow(obj.windowHandle):
					log.info(
						"Determines the devInfo that is forced to be a good UIA window object:\n%s"
						% "\n".join(obj.devInfo)
					)
					obj.appModule.isGoodUIAWindow = lambda hwnd: True
		except AttributeError:
			pass
