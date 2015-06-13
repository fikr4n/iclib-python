#!/usr/bin/python3

from iclib.hijri import ummqura


def ummqura_gregorian():
	d = (1436, 1, 1)
	print(d, '->', ummqura.to_gregorian(*d))

def gregorian_ummqura():
	d = (2015, 1, 1)
	print(d, '->', ummqura.from_gregorian(*d))

loc = sorted(locals().items())
for k,v in loc:
	if not k.startswith('_') and callable(v):
		print('-' * 5, k, '-' * 5)
		v()
		print()

