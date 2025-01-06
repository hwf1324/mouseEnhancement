# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 hwf1324 <1398969445@qq.com>

import controlTypes
import globalPluginHandler


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		try:
			if (
				(
					obj.windowClassName == "Microsoft.UI.Content.DesktopChildSiteBridge"
					or obj.windowClassName == "Windows.UI.Composition.DesktopWindowContentBridge"
				)
				and obj.role == controlTypes.Role.PANE
				and not obj.appModule.isGoodUIAWindow(obj.windowHandle)
			):
				obj.appModule.isGoodUIAWindow = lambda hwnd: True
		except AttributeError:
			pass
