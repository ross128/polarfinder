#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from math import cos, sin
import os
import configparser
import ephem

class PolarFinder(tk.Tk):
	"""Polar finder window"""

	def __init__(self, size=400, configfile='~/.config/polarfinder.ini'):
		super(PolarFinder, self).__init__()
		self.wm_title('PolarFinder')
		self.configure(background='#000000')
		self.size = size

		#configuration
		self.configfile = os.path.expanduser(configfile)
		self.config = configparser.ConfigParser()
		self.config.read(self.configfile)

		#canvas for drawing circle
		self.canvas = tk.Canvas(self, width=self.size, height=self.size, background='#000000', highlightthickness=0)
		self.canvas.grid(row=0, columnspan=2, sticky=tk.N)

		#label for Local Sidereal Time
		self.lst_label = tk.Label(self, background='#000000', foreground='#ff0000')
		self.lst_label.grid(row=1, columnspan=2)

		#label for Hour Angle
		self.hour_angle_label = tk.Label(self, background='#000000', foreground='#ff0000')
		self.hour_angle_label.grid(row=2, columnspan=2)

		#latitude input
		self.latitude = tk.StringVar(value=self.config.get('observer', 'latitude', fallback=0.0))
		self.latitude.trace('w', lambda *args: self.update_config())
		self.lat_label = tk.Label(self, text='Latitude:', background='#000000', foreground='#ff0000')
		self.lat_label.grid(row=3, column=0, sticky=tk.E, pady=10)
		self.lat_input = tk.Entry(self, textvariable=self.latitude, background='#000000', foreground='#ff0000', highlightbackground='#ff0000')
		self.lat_input.grid(row=3, column=1, sticky=tk.W)

		#longitude input
		self.longitude = tk.StringVar(value=self.config.get('observer', 'longitude', fallback=0.0))
		self.longitude.trace('w', lambda *args: self.update_config())
		self.lon_label = tk.Label(self, text='Longitude:', background='#000000', foreground='#ff0000')
		self.lon_label.grid(row=4, column=0, sticky=tk.E)
		self.lon_input = tk.Entry(self, textvariable=self.longitude, background='#000000', foreground='#ff0000', highlightbackground='#ff0000')
		self.lon_input.grid(row=4, column=1, sticky=tk.W)

		self.update()

	def update_config(self):
		#update config file
		if not self.config.has_section('observer'):
			self.config.add_section('observer')
		self.config.set('observer', 'longitude', self.longitude.get())
		self.config.set('observer', 'latitude', self.latitude.get())
		with open(self.configfile, 'w') as cf:
			self.config.write(cf)

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

		#update ephem
		observer = ephem.Observer()
		observer.epoch = ephem.now()
		observer.date = ephem.now()
		observer.lat = self.config.get('observer', 'latitude')
		observer.lon = self.config.get('observer', 'longitude')

		polaris = ephem.star('Polaris')
		polaris.compute(observer)
		ha = ephem.hours(observer.sidereal_time() - polaris.a_ra).norm

		#labels
		self.lst_label.config(text='Local Sidereal Time: ' + str(observer.sidereal_time()))
		self.hour_angle_label.config(text='Polaris Hour Angle: ' + str(ha))

		#update every second
		self.after(1000, self.update)

if __name__ == "__main__":
	window = PolarFinder()
	window.mainloop()
