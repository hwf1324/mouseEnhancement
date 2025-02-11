# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2024 hwf1324 <1398969445@qq.com>

import controlTypes
import globalPluginHandler
from NVDAObjects import NVDAObject


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def event_mouseMove(self, obj: NVDAObject, nextHandler, x: int, y: int):
		try:
			if (
				obj.appModule.appName.startswith("git-")
				and obj.appModule.appName.endswith("-bit")
				and obj.role == controlTypes.Role.PANE
				and obj.name is None
			):
				obj.name = obj.displayText
		except AttributeError:
			pass

		nextHandler()
