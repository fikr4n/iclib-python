#!/usr/bin/python3

from iclib import qibla


def istiqlal():
	lat = -6.169777778
	lng = 106.8307333
	print('Masjid Istiqlal, Jakarta, Indonesia')
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng))
	print(qibla.direction_str(lat, lng))

def yogyakarta():
	lat = -(7 + 48 / 60.0)
	lng = 110 + 21 / 60.0
	print('Yogyakarta, Indonesia')
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng))
	print(qibla.direction_str(lat, lng))

loc = sorted(locals().items())
for k,v in loc:
	if not k.startswith('_') and callable(v):
		print('-' * 5, k, '-' * 5)
		v()
		print()

