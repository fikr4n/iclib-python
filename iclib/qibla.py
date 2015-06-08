# -*- coding: utf-8 -*-
from . import formula

def direction(lat, lng):
	return formula.qibla(lat, lng)

def direction_dms(lat, lng):
	return _dms(formula.qibla(lat, lng))

def direction_str(lat, lng, prec=0):
	d, m, s = direction_dms(lat, lng)
	# negative input might returns wrong result
	return '{}° {}\' {:.{}f}"'.format(d, m, s, prec)

def _dms(deg):
	seconds = deg * 3600
	m, s = divmod(seconds, 60)
	d, m = divmod(m, 60)
	return (int(d), int(m), s)
