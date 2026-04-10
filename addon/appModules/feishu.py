# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 hwf1324 <1398969445@qq.com>

"""飞书 appModule"""

import appModuleHandler
import controlTypes
import IAccessibleHandler
import winUser
from comtypes import COMError
from NVDAObjects import NVDAObject
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible.chromium import Document
from NVDAObjects.IAccessible.ia2Web import Ia2Web


class RedirectDocument(Ia2Web):
	def objectFromPointRedirect(self, x: int, y: int):
		docObj: Document = self.parent.lastChild
		try:
			redirect = docObj.IAccessibleObject.accHitTest(x, y)
		except COMError:
			return None

		if not redirect:
			return None

		redirect = IAccessibleHandler.normalizeIAccessible(redirect)
		obj: IAccessible = IAccessible(IAccessibleObject=redirect, IAccessibleChildID=winUser.CHILDID_SELF)

		return obj


class AppModule(appModuleHandler.AppModule):
	# def isGoodUIAWindow(self, hwnd):
	# 	return True

	def chooseNVDAObjectOverlayClasses(self, obj: NVDAObject, clsList: list[type[NVDAObject]]):
		if obj.role == controlTypes.Role.GROUPING and obj.name == "PageContainerContentsView":
			clsList.insert(0, RedirectDocument)
