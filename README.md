# ICLib Python
Islamic Calculation Library (ICLib) contains calculations/algorithms needed specifically by muslims and people in muslim countries, such as salat (prayer) times, qibla direction, and Hijri conversion.

## Introduction

This library is inspired by [Islamic Tools Library (ITL)](http://projects.arabeyes.org/project.php?proj=ITL) which seems no longer be maintained. ITL is LGPL-licensed, so you cannot use it for closed source applications if you cannot provide an easy way for the users (of the application, not the developer who uses the library) to change and modify the library used in your application. ICLib is written from "zero" and aims to be more flexible by providing more programming languages and using Apache license, so you can use it even for closed source commercial applications _as long as_ it is for good deeds. I don't know if we need to use modified Apache license to state that limitation :).

Calculation of **prayer times** and **qibla direction** is based on **Dr. Eng. Rinto Anugraha, M.Si.** from Universitas Gadjah Mada, Indonesia (published in 2012 AD), and also refer to **Pedoman Hisab Muhammadiyah** (published in 1430 AH / 2009 AD), **Wikipedia** (English version), etc for comparison and complement. **Umm al-Qura Hijri calendar** month lengths table is based on the output of ITL (not the source code).

After releasing this Python version, we plan to make the C and Java version, and probably other languages. We also plan to implement hilal (crescent) altitude calculation for new moon estimation (not as reference for ibadah).

### Notes on Hijri conversion

Any Hijri conversion including Umm al-Qura is not used as reference for ibadah e.g. beginning of saum (fasting), Eid al-Fitr, and Eid al-Adha.

## Usage example

Latitude and longitude are in degrees, positive values for north and east respectively, negative values for south and west respectively. More examples are available in `example-*.py`.

```python
	from iclib import salat
	import datetime
	
	date = datetime.date.today()
	c = (salat.TimeCalculator().date(date)
		# latitude, longitude, altitude/height, timezone
		.location(-6.38043079, 106.85337984, 0, +7)
		.method('egypt'))
	t = c.calculate()
	for i in t:
		print(i) # as datetime.time
	
	# other styles
	print(t.zuhr) # as datetime.time
	print(t.get_time(salat.ASR)) # as datetime.time
	print(t.get_hms(salat.MAGHRIB)) # as tuple of int (hour, minute, second)
	print(t.get_hm(salat.ISHA)) # as tuple of int (hour, minute)
```

```python
	from iclib import qibla
	
	lat = -6.169777778
	lng = 106.8307333
	print(qibla.direction(lat, lng)) # in degrees from the north (clock-wise)
	print(qibla.direction_dms(lat, lng)) # deg, min, sec (as tuple)
	print(qibla.direction_str(lat, lng)) # deg° min' sec" (as str)
```

```python
	from iclib.hijri import ummqura

	print(ummqura.to_gregorian(1436, 1, 1)) # year, month, day
	print(ummqura.from_gregorian(2015, 1, 1)) # year, month, day
```

_We need your dua and support_

**Salam and have fun!**
