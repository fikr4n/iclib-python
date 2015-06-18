#!/usr/bin/python3

from iclib import qibla


def istiqlal():
	lat = -6.169777778
	lng = 106.8307333
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng))
	print(qibla.direction_str(lat, lng))

def yogyakarta():
	lat = -(7 + 48 / 60.0)
	lng = 110 + 21 / 60.0
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng))
	print(qibla.direction_str(lat, lng))

def nearnorthpole():
	lat = 89
	lng = 39.82616111
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng))
	print(qibla.direction_str(lat, lng))

def nearsouthpole():
	lat = -89
	lng = 39.82616111
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng))
	print(qibla.direction_str(lat, lng))

def makkah_east():
	lat = 21.42250833
	lng = 40
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng))
	print(qibla.direction_str(lat, lng))

def makkah_west():
	lat = 21.42250833
	lng = 39
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng))
	print(qibla.direction_str(lat, lng))

loc = sorted(locals().items())
for k,v in loc:
	if not k.startswith('_') and callable(v):
		print('-' * 5, k, '-' * 5)
		v()
		print()

