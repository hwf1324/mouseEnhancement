# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 hwf1324 <1398969445@qq.com>

"""Firefox appModule.
Used to report information about tabs in the Tree Style Tab extension when the mouse moves."""

import time

import appModuleHandler
import config
import controlTypes
import mouseHandler
import ui
from NVDAObjects.IAccessible.mozilla import Mozilla


class AppModule(appModuleHandler.AppModule):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.mouseMessage = None

	def event_mouseMove(self, obj: Mozilla, nextHandler, x: int, y: int):
		nextHandler()
		if (
			config.conf["vision"]["autoUpdateMouseObject"]["updateMethod"] == "coreCycle"
			and mouseHandler.lastMouseEventTime >= time.time() - 0.1  # Reduced frequency of reporting
		):
			return
		if obj.name is None and obj.childCount == 0 and obj.parent.role == controlTypes.Role.LISTITEM:
			mouseMessage = obj.parent.name
			if mouseMessage != self.mouseMessage:
				ui.message(mouseMessage)
				self.mouseMessage = mouseMessage
