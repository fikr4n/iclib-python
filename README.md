# ICLib Python
Islamic Calculation Library (ICLib) contains calculations/algorithms needed specifically by muslims, such as salat (prayer) times, qibla direction, and Hijri conversion for Python.

## Introduction

This library is inspired by [Islamic Tools Library (ITL)](http://projects.arabeyes.org/project.php?proj=ITL) which seems no longer be maintained. I don't know if they got shaheed or something else. ITL is LGPL-licensed, so you cannot use it for closed source applications if you cannot provide an easy way for the users (of the application, not the developer who uses the library) to change and modify the library used in your application. ICLib is written from "zero" and aims to be more flexible by providing more programming languages (still planned) and using Apache license, so you can use it even for closed source commercial applications _as long as_ it is for good deeds. I don't know if we need to use modified Apache license to state that limitation :).

Currently only salat times calculation has been provided, others will be available soon inshaallah. After releasing this Python version, we plan to make the C and Java version, and probably other languages.

## Usage example

```python
	from iclib import salat
	import datetime
	
	date = datetime.date.today()
	c = salat.TimeCalculator().date(date) \
		.location(-6.38043079, 106.85337984, 0, 7) \
		.method('egypt')
	t = c.calculate()
	for i in t:
		print(i)
	
	# or by name:
	print(t.zuhr)
```

_We need your dua and support_

**Salam and have fun!**
