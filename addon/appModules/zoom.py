# mouseEnhancement add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.
# Copyright (C) 2025 hwf1324 <1398969445@qq.com>

"""Zoom appModule"""

from nvdaBuiltin.appModules.zoom import *  # noqa: F403


class AppModule(AppModule):  # noqa: F405
	def isGoodUIAWindow(self, hwnd):
		return True
