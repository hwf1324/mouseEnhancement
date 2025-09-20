# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 hwf1324 <1398969445@qq.com>

"""Windows Terminal appModule"""

from contextlib import contextmanager
from collections.abc import Callable

import appModuleHandler
import controlTypes
from NVDAObjects import UIA
from textInfos import UNIT_LINE, UNIT_PARAGRAPH


@contextmanager
def restrictParagraphToLine():
	import config

	try:
		curTextUnit = config.conf["mouse"]["mouseTextUnit"]
		if curTextUnit == UNIT_PARAGRAPH:
			config.conf["mouse"]["mouseTextUnit"] = UNIT_LINE
		yield
	finally:
		config.conf["mouse"]["mouseTextUnit"] = (
			curTextUnit or config.conf.getConfigValidation(("mouse", "mouseTextUnit")).default
		)


class AppModule(appModuleHandler.AppModule):

	def event_mouseMove(self, obj: UIA.UIA, nextHandler: Callable[[], None], x: int, y: int) -> None:
		if obj.role == controlTypes.Role.TERMINAL:
			with restrictParagraphToLine():
				nextHandler()
			return
		nextHandler()
