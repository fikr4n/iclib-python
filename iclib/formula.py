# Convention for internal/basic formula:
# - short param name, mid-length method name
# - no structure/class, only basic/primitives known in majority of languages
# - procedural
# - constants only for very limited choices (asr shadow ratio)
# - no param (type, value, range, etc) checking
# - no exception raising/throwing
# - use decimal separator for number in floating-point-aware division
# - no method overloading
# - casing follows language convention
# Note:
# - all angles are "currently" in degrees instead of radians
# - all length (actually only h) are in meters
# - all times are in hours
# - month and day start from 1, weekday start from 0 (Ahad/Sunday)

import math


ASR_RATIO_MAJORITY = 1
ASR_RATIO_HANAFI = 2


def zuhr   (lng, tz, et):
	return 12 + tz - lng / 15.0 - et

def asr    (t_zuhr, lat, ds, asr_ratio):
	alt = _acot_deg(asr_ratio + _tan_deg(abs(ds - lat))) # altitude of the sun
	return t_zuhr + hour_angle(lat, alt, ds) / 15.0

def maghrib(t_zuhr, lat, ds, h):
	alt = -0.8333 - 0.0347 * math.sqrt(h)
	return t_zuhr + hour_angle(lat, alt, ds) / 15.0

def isha   (t_zuhr, lat, ds, isha_angle):
	alt = -isha_angle
	return t_zuhr + hour_angle(lat, alt, ds) / 15.0

def fajr   (t_zuhr, lat, ds, fajr_angle):
	alt = -fajr_angle
	return t_zuhr - hour_angle(lat, alt, ds) / 15.0

def sunrise(t_zuhr, lat, ds, h):
	alt = -0.8333 - 0.0347 * math.sqrt(h) # equals to maghrib
	return t_zuhr - hour_angle(lat, alt, ds) / 15.0

def hour_angle(lat, alt, ds):
	"""Return hour angle in degrees"""
	cos_ha = ((_sin_deg(alt) - _sin_deg(lat) * _sin_deg(ds))
		/     (                _cos_deg(lat) * _cos_deg(ds)))
	if -1 <= cos_ha <= 1:
		return _acos_deg(cos_ha)
	else:
		return float('nan')

def eq_time(jd):
	"""Return Equation of Time in hours"""
	u = (jd - 2451545) / 36525.0
	l0 = 280.46607 + 36000.7698 * u # average longitude of the sun in degrees
	return (
		-(1789 + 237 * u) * _sin_deg(l0) 
		- (7146 - 62 * u) * _cos_deg(l0) 
		+ (9934 - 14 * u) * _sin_deg(2 * l0) 
		- (29 +    5 * u) * _cos_deg(2 * l0) 
		+ (74 +   10 * u) * _sin_deg(3 * l0) 
		+ (320 -   4 * u) * _cos_deg(3 * l0) 
		- 212             * _sin_deg(4 * l0)) / 60000.0

def decl_sun(jd):
	"""Return Declination of the sun in degrees"""
	t = 2 * math.pi * (jd - 2451545) / 365.25 # angle of date
	return (0.37877
		+ 23.264  * _sin_deg(    57.297 * t - 79.547)
		+ 0.3812  * _sin_deg(2 * 57.297 * t - 82.682)
		+ 0.17132 * _sin_deg(3 * 57.297 * t - 59.722))

def gregorian_to_jd(y, m, d):
	"""Return Julian Day of a Gregorian or Julian date"""
	if m <= 2:
		m += 12; y -= 1
	if y > 1582 or (y == 1582 and (m > 10 or (m == 10 and d >= 15))):
		# first gregorian is 15-oct-1582
		a = math.floor(y / 100.0)
		b = 2 + math.floor(a / 4.0) - a
	else: # invalid dates (5-14) are also considered as julian
		b = 0
	abs_jd = (1720994.5 + math.floor(365.25 * y) + math.floor(30.6001 * (m + 1))
		+ d + b)
	# negative year is okay, negative julian day might be wrong (i.e. y < -4712)
	return abs_jd

def jd_to_gregorian(jd):
	jd1 = jd + 0.5
	z = math.floor(jd1)
	f = jd1 - z
	if z < 2299161:
		a = z
	else:
		aa = math.floor((z - 1867216.25) / 36524.25)
		a = z + 1 + aa - math.floor(aa / 4.0)
	b = a + 1524
	c = math.floor((b - 122.1) / 365.25)
	d = math.floor(365.25 * c)
	e = math.floor((b - d) / 30.6001)
	day = b - d - math.floor(30.6001 * e) + f
	month = e - 1 if e < 14 else e - 13
	year = c - 4715 if month <= 2 else c - 4716
	return (int(year), int(month), int(day), jd_to_weekday(jd))

def jd_to_weekday(jd):
	return int(math.floor(jd + 1.5) % 7)

def adjust_jd_hour(jd, hours):
	return jd + hours / 24.0

def qibla(lat, lng):
	"""Return qibla direction in degrees from the north (clock-wise)"""
	lng_a = 39.82616111
	lat_a = 21.42250833
	deg = _atan2_deg(_sin_deg(lng_a - lng),
		_cos_deg(lat) * _tan_deg(lat_a)
		- _sin_deg(lat) * _cos_deg(lng_a - lng))
	return deg if deg > 0 else deg + 360

def _sin_deg(deg):
	return math.sin(math.radians(deg))

def _cos_deg(deg):
	return math.cos(math.radians(deg))

def _acos_deg(x_r):
	return math.degrees(math.acos(x_r))

def _tan_deg(deg):
	return math.tan(math.radians(deg))

def _acot_deg(x_y):
	return math.degrees(math.atan(1.0 / x_y))

def _atan2_deg(y, x):
	return math.degrees(math.atan2(y, x))

