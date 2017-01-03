#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk


class PolarFinder(tk.Tk):
	"""Polar finder window"""

	def __init__(self):
		super(PolarFinder, self).__init__()
		self.wm_title('PolarFinder')
		self.configure(background='#000000')


if __name__ == "__main__":
	window = PolarFinder()
	window.mainloop()
