#!/usr/bin/python3
from iclib import salat
import datetime as dt
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from PIL.ImageColor import getrgb as rgb
import sys

def xlen(start, stop, step):
	"""Number of items `frange` will generate"""
	return sum(1 for _ in frange(start, stop, step))

def frange(start, stop, step):
	"""Float version of `range`"""
	f = 1 / step
	return (i / f for i in range(int(start * f), int(stop * f), int(step * f)))

def to_color(times):
	"""Color representation of extreme (could not calculate) salat times"""
	m = times.times
	# fajr (½red), isha (½red), sunrise (½green), maghrib (½green), asr (blue)
	r1, r2, g1, g2, b = 0, 0, 0, 0, 0
	if   m[salat.FAJR]    ==  inf: r1 =  0x44
	elif m[salat.FAJR]    == -inf: r1 = -0x44
	if   m[salat.ISHA]    ==  inf: r2 = -0x44
	elif m[salat.ISHA]    == -inf: r2 =  0x44
	if   m[salat.SUNRISE] ==  inf: g1 =  0x44
	elif m[salat.SUNRISE] == -inf: g1 = -0x44
	if   m[salat.MAGHRIB] ==  inf: g2 = -0x44
	elif m[salat.MAGHRIB] == -inf: g2 =  0x44
	if   m[salat.ASR]     ==  inf: b  = -0x88
	elif m[salat.ASR]     == -inf: b  =  0x88
	return r1, r2, g1, g2, b

METHOD = sys.argv[1]
DAYS = (0, 365, 5/1)  # horizontal frange
WIDTH = xlen(*DAYS)
LATS = (90, -90 - 1/1, -1/1)  # vertical frange
HEIGHT = xlen(*LATS)
inf = float('inf')

if __name__ == '__main__':
	pixels = []
	c = salat.TimeCalculator().method(METHOD)

	for lat in frange(*LATS):  # horizontal line from top to bottom
		if lat % 15 == 0:  # draw only horizontal separator
			pixels.extend((rgb('#333333'),) * (6 * WIDTH + 5))
			continue
		
		c.location(lat, 0, 0, 0)
		row = [to_color(c.date(dt.datetime(2015, 1, 1) + dt.timedelta(yday)).calculate())
			for yday in frange(*DAYS)]
		for p in row:  # fajr
			pixels.append((p[0]*2 + 0x88,) * 3)
		pixels.append(rgb('#333333'))
		for p in row:  # isha
			pixels.append((p[1]*2 + 0x88,) * 3)
		pixels.append(rgb('#333333'))
		for p in row:  # sunrise
			pixels.append((p[2]*2 + 0x88,) * 3)
		pixels.append(rgb('#333333'))
		for p in row:  # maghrib
			pixels.append((p[3]*2 + 0x88,) * 3)
		pixels.append(rgb('#333333'))
		for p in row:  # asr
			pixels.append((p[4] + 0x88,) * 3)
		pixels.append(rgb('#333333'))
		for p in row:  # all
			pixels.append((p[0] + p[1] + 0x88, p[2] + p[3] + 0x88, p[4] + 0x88))
	ximg = PIL.Image.new('RGB', (6 * WIDTH + 5, HEIGHT))
	ximg.putdata(pixels)
	draw = PIL.ImageDraw.Draw(ximg)
	font = PIL.ImageFont.load_default()
	for i, name in enumerate(('FAJR', 'ISHA', 'SUNRISE', 'MAGRIB', 'ASR', 'MIXED')):
		w, h = draw.textsize(name, font)
		draw.text(((i+0.5) * (WIDTH+1) - w/2, HEIGHT/2 - h/2), name,
			fill=(0xff, 0xff, 0xff), font=font)
	
	world = PIL.Image.open('Tissot_indicatrix_world_map_equirectangular_proj_by_Eric_Gaba_from_wikimedia.png', 'r')
	world = world.resize((WIDTH*2, HEIGHT), PIL.Image.ANTIALIAS)
	draw = PIL.ImageDraw.Draw(world)
	for y in range(0, world.size[1], 15):
		draw.line([0, y, world.size[0], y], rgb('#333333'), 1)
	
	img = PIL.Image.new('RGB', (ximg.size[0] + world.size[0], HEIGHT))
	img.paste(world, (0, 0))
	img.paste(ximg, (world.size[0], 0))
	img.save('generate_extreme_' + METHOD + '.png')

