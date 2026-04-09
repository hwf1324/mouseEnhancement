# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2024-2025 hwf1324 <1398969445@qq.com>

import threading
import time
from ctypes.wintypes import POINT

import config
import controlTypes
import globalPluginHandler
import IAccessibleHandler
import mouseHandler
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

_redirect_cache_pos: tuple[int, int] | None = None
_redirect_cache_element = None
_redirect_cache_time: float = 0.0
_REDIRECT_CACHE_DISTANCE = 5
_REDIRECT_CACHE_TIMEOUT = 0.5

_window_class_cache: dict[int, str] = {}


def _get_cached_class_name(hwnd: int) -> str:
	cls_name = _window_class_cache.get(hwnd)
	if cls_name is None:
		cls_name = winUser.getClassName(hwnd)
		_window_class_cache[hwnd] = cls_name
		if len(_window_class_cache) > 256:
			_window_class_cache.clear()
	return cls_name


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
		global _redirect_cache_pos, _redirect_cache_element, _redirect_cache_time

		now = time.time()
		if (
			_redirect_cache_pos is not None
			and _redirect_cache_element is not None
			and (now - _redirect_cache_time) < _REDIRECT_CACHE_TIMEOUT
			and abs(x - _redirect_cache_pos[0]) <= _REDIRECT_CACHE_DISTANCE
			and abs(y - _redirect_cache_pos[1]) <= _REDIRECT_CACHE_DISTANCE
		):
			try:
				return UIA(UIAElement=_redirect_cache_element)
			except COMError:
				_redirect_cache_element = None

		result: list = [None]
		done_event = threading.Event()

		def wrapper():
			try:
				result[0] = UIAHandler.handler.clientObject.ElementFromPointBuildCache(
					POINT(x, y), mouseCacheRequest
				)
			except COMError:
				pass
			finally:
				done_event.set()

		UIAHandler.handler.MTAThreadQueue.put(wrapper)
		done_event.wait(timeout=0.2)

		if result[0] is None:
			return None

		_redirect_cache_pos = (x, y)
		_redirect_cache_element = result[0]
		_redirect_cache_time = now
		return UIA(UIAElement=result[0])


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def chooseNVDAObjectOverlayClasses(self, obj: NVDAObject, clsList: list[type[NVDAObject]]):
		try:
			if obj.role == controlTypes.Role.PANE:
				if (  # Electron
					isinstance(obj, IAccessible)
					and _get_cached_class_name(obj.IA2WindowHandle) == "Chrome_WidgetWin_1"
					and obj.IA2Attributes in (
						ELECTRON_IA2_ATTRIBUTES,
						CHROME_SIDEBAR_EXTENSION_IA2_ATTRIBUTES,  # Chrome's Sidebar
					)
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
			if (  # Tauri (WebView2)
				isinstance(obj, IAccessible)
				and obj.windowClassName == "Chrome_RenderWidgetHostHWND"
				and getattr(obj.parent, "windowClassName", "").startswith("TAURI_")
			):
				clsList.insert(0, RedirectChromiumUIA)
		except AttributeError:
			pass

	def event_mouseMove(self, obj: NVDAObject, nextHandler, x: int, y: int):
		if (
			config.conf["vision"]["autoUpdateMouseObject"]["updateMethod"] == "coreCycle"
			and mouseHandler.lastMouseEventTime >= time.time() - (config.conf["vision"]["autoUpdateMouseObject"]["mouseMoveEventDelay"] / 1000)
		):
			return
		nextHandler()
