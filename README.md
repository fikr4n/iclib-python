# ICLib Python
Islamic Calculation Library (ICLib) contains calculations/algorithms needed specifically by muslims and people in muslim countries, such as salat (prayer) times, qibla direction, and Hijri conversion.

## Introduction

This library is inspired by [Islamic Tools Library (ITL)](http://projects.arabeyes.org/project.php?proj=ITL) which seems no longer be maintained. ITL is LGPL-licensed, so you cannot use it for closed source applications if you cannot provide an easy way for the users (of the application, not the developer who uses the library) to change and modify the library used in your application. ICLib is written from "zero" and aims to be more flexible by providing more programming languages and using Apache license, so you can use it even for closed source commercial applications _as long as_ it is for good deeds. I don't know if we need to use modified Apache license to state that limitation :).

Calculation of **prayer times** and **qibla direction** is based on **Dr. Eng. Rinto Anugraha, M.Si.** from Universitas Gadjah Mada, Indonesia (published in 2012 AD), and also refer to **Pedoman Hisab Muhammadiyah** (published in 1430 AH / 2009 AD), **Wikipedia** (English version), etc for comparison and complement. **Umm al-Qura Hijri calendar** month lengths table is based on the output of ITL (not the source code).

This library is written in Python, see also the [Java](https://github.com/fikr4n/iclib-java) version. We plan to make the C version, and probably other languages. We also plan to implement hilal (crescent) altitude calculation for new moon estimation (not as reference for ibadah).

**Notes on Hijri conversion**

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

## Calculation method choices

For Asr, you can choose between "Majority" and "Hanafi". According to the study of the majority of scholars (_Jumhur Ulama_), including Imam Shafi'i, based on Hadith Asr is when the length of shadow **equals** to the length of the object, plus the length of the shadow at midday. However, according to the study of Imam Hanafi, the length of shadow is **twice** the length of the object, plus the length of the shadow at midday.

For Fajr and Isha, there are difference (scientific) opinions about the angle of the Sun (below the horizon) at those time. These are some Islamic institution standards you can choose. Some is not implemented yet, but you can set it manually. _(Copied from [itl-java](https://github.com/fikr4n/itl-java) README file)_

- **Egyptian General Authority of Survey**; usually used in Indonesia, Iraq, Jordan, Lebanon, Malaysia, Singapore, Syria, parts of Africa, and parts of United States.
- **University of Islamic Sciences**, Karachi (Shafi'i); usually used in Iran, Kuwait, and parts of Europe.
- **University of Islamic Sciences**, Karachi (Hanafi); usually used in Afghanistan, Bangladesh, and India.
- **Islamic Society of North America**; usually used in Canada, Parts of UK, and parts of United States.
- **Muslim World League (MWL)**; usually used in parts of Europe, Far East, and parts of United States.
- **Umm Al-Qurra University**; usually used in Saudi Arabia.
- Fixed Ishaa Angle Interval (always 90); usually used in Bahrain, Oman, Qatar, United Arab Emirates.

There are locations near the poles having extreme latitude where some salat times cannot be calculated. For example, if location L is always night on date D1 till D2, we cannot calculate sunrise and maghrib for those days. Those extreme latitudes accross a (gregorian) year is displayed in black and white in attached images `generate_extreme_*.png`. Solution for these locations is by using estimation or approach. Please read the literatures about this.

![egypt](https://raw.githubusercontent.com/fikr4n/iclib-python/master/generate_extreme_egypt.png)
_Extreme latitude based on 'egypt' method_

More about prayer times, you can learn from Kitabs of Fiqih or online resource.

## Further reading

- Waktu Shalat (Bahasa Indonesia) [1](http://rumaysho.com/shalat/waktu-shalat-1-shalat-zhuhur-2932.html) [2](http://rumaysho.com/shalat/waktu-shalat-2-shalat-ashar-2936.html) [3](http://rumaysho.com/shalat/waktu-shalat-3-shalat-maghrib-2940.html) [4](http://rumaysho.com/shalat/waktu-shalat-4-shalat-isya-2944.html) [5](http://rumaysho.com/shalat/waktu-shalat-5-shalat-shubuh-2948.html)

---

_We need your dua and support_

**Salam and have fun!**
