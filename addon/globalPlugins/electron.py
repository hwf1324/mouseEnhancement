# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2024 hwf1324 <1398969445@qq.com>

import controlTypes
import globalPluginHandler
import IAccessibleHandler
import winUser
from NVDAObjects import NVDAObject
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible.chromium import Document
from NVDAObjects.IAccessible.ia2Web import Ia2Web


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

	def chooseNVDAObjectOverlayClasses(self, obj: Ia2Web, clsList: list[NVDAObject]):
		try:
			if (
				obj.windowClassName.startswith("Chrome_")
				and obj.role == controlTypes.Role.PANE
				and obj.previous
				and obj.previous.lastChild
				and obj.previous.lastChild.windowClassName == "Chrome_RenderWidgetHostHWND"
			):
				clsList.insert(0, RedirectDocument)
		except AttributeError:
			pass
