#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from math import cos, sin
import ephem

class PolarFinder(tk.Tk):
	"""Polar finder window"""

	def __init__(self, size=400):
		super(PolarFinder, self).__init__()
		self.wm_title('PolarFinder')
		self.configure(background='#000000')
		self.size = size

		#canvas for drawing circle
		self.canvas = tk.Canvas(self, width=self.size, height=self.size, background='#000000', highlightthickness=0)
		self.canvas.pack(side=tk.TOP)

		self.update()

	def update(self):
		"""update the PolarFinder window"""

		#clear canvas
		self.canvas.delete("all")

		#center
		c_x = c_y = self.size/2

		#compute radii
		r_max = (self.size-10)/2
		r = list(map(lambda n: r_max*(1-n*0.035), range(7)))

		#circles
		for i in range(2,5):
			self.canvas.create_oval(c_x-r[i], c_y-r[i], c_x+r[i], c_y+r[i], outline='#ff0000')

		#ticks
		nticks = 48
		for i,theta in enumerate(map(lambda n:2*n*ephem.pi/nticks, range(nticks+1))):
			theta += ephem.pi/2
			if i%6==0:
				self.canvas.create_line(c_x+r[0]*cos(theta), c_y-r[0]*sin(theta), c_x+r[6]*cos(theta), c_y-r[6]*sin(theta), fill="#ff0000", width=2)
			else:
				self.canvas.create_line(c_x+r[1]*cos(theta), c_y-r[1]*sin(theta), c_x+r[5]*cos(theta), c_y-r[5]*sin(theta), fill="#ff0000", width=1)



if __name__ == "__main__":
	window = PolarFinder()
	window.mainloop()
