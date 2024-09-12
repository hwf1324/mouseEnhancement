# mouseEnhancements add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2024 hwf1324 <1398969445@qq.com>

"""PDFgear appModule.
"""

import appModuleHandler
import controlTypes
from NVDAObjects import NVDAObject


class AppModule(appModuleHandler.AppModule):
	def event_NVDAObject_init(self, obj: NVDAObject):
		if controlTypes.Role.BUTTON == obj.role and not obj.name:
			obj.name = obj.lastChild.name
