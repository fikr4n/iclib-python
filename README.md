# ICLib Python
Islamic Calculation Library (ICLib) contains calculations/algorithms needed specifically by muslims and people in muslim countries, such as salat (prayer) times, qibla direction, and Hijri conversion.

## Introduction

This library is inspired by [Islamic Tools Library (ITL)](http://projects.arabeyes.org/project.php?proj=ITL) which seems no longer be maintained. I don't know if they got shaheed or something else. ITL is LGPL-licensed, so you cannot use it for closed source applications if you cannot provide an easy way for the users (of the application, not the developer who uses the library) to change and modify the library used in your application. ICLib is written from "zero" and aims to be more flexible by providing more programming languages (still planned) and using Apache license, so you can use it even for closed source commercial applications _as long as_ it is for good deeds. I don't know if we need to use modified Apache license to state that limitation :).

Currently only salat times and qibla direction calculation have been provided, others will be available soon inshaallah. After releasing this Python version, we plan to make the C and Java version, and probably other languages.

## Usage example

Latitude and longite are in degrees, positive values for north and east, negative values for south and west.

```python
	from iclib import salat
	import datetime
	
	date = datetime.date.today()
	c = salat.TimeCalculator().date(date) \
		.location(-6.38043079, 106.85337984, 0, +7) \ # lat, lng, alt, timezone
		.method('egypt')
	t = c.calculate()
	for i in t:
		print(i)
	
	# other styles
	print(t.zuhr)
	print(t.get_time(salat.ASR))
	print(t.get_hms(salat.MAGHRIB)) # hour, minute, second
	print(t.get_hm(salat.ISHA)) # hour, minute
```

```python
	from iclib import qibla
	
	lat = -6.169777778
	lng = 106.8307333
	print(qibla.direction(lat, lng))
	print(qibla.direction_dms(lat, lng)) # degree, arc minute, arc second
	print(qibla.direction_str(lat, lng)) # degree° minute' second"
```

_We need your dua and support_

**Salam and have fun!**
