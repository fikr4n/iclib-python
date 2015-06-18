#!/usr/bin/python3

from iclib.hijri import ummqura


def ummqura_gregorian():
	d = (1436, 1, 1)
	print(d, '->', ummqura.to_gregorian(*d))

def ummqura_gregorian_first():
	print(ummqura.to_gregorian(1420, 1, 1))

def ummqura_gregorian_last():
	print(ummqura.to_gregorian(1450, 12, 30))

def gregorian_ummqura():
	d = (2015, 1, 1)
	print(d, '->', ummqura.from_gregorian(*d))

def gregorian_ummqura_first():
	print(ummqura.from_gregorian(1999, 4, 17))

def gregorian_ummqura_last():
	print(ummqura.from_gregorian(2029, 5, 14))

loc = sorted(locals().items())
for k,v in loc:
	if not k.startswith('_') and callable(v):
		print('-' * 5, k, '-' * 5)
		v()
		print()

