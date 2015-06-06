from . import formula
import datetime
import math
import collections


STANDARD_ANGLES = {
	# (fajr_deg, isha_deg)
	'mwl': (18, 17),
	'isna': (15, 15),
	'egypt': (19.5, 17.5),
	'karachi': (18, 18),
	'muhammadiyah': (20, 18),
}

N = 6
FAJR, SUNRISE, ZUHR, ASR, MAGHRIB, ISHA = range(N)


class TimeCalculator(object):

	def method(self, angle, asr_ratio=None, adjustments={ZUHR: 2.0/60}):
		if type(angle) is str:
			self.fajr_angle, self.isha_angle = STANDARD_ANGLES[angle]
		else:
			self.fajr_angle, self.isha_angle = angle
		if asr_ratio == 'hanafi':
			self.asr_ratio = formula.ASR_RATIO_HANAFI
		else:
			self.asr_ratio = formula.ASR_RATIO_MAJORITY
		self.adjustments = tuple(adjustments.get(k, 0) for k in range(N))
		return self

	def location(self, lat, lng, h, tz):
		self.lat = lat
		self.lng = lng
		self.h = h
		if isinstance(tz, datetime.tzinfo):
			self.tz = tz.utcoffset(None).total_seconds() / 3600.0
		else:
			self.tz = tz
		return self

	def date(self, date):
		self.d = date
		return self

	def date_relative(self, days):
		if not isinstance(days, datetime.timedelta):
			days = datetime.timedelta(days)
		self.d += days
		return self

	def calculate(self):
		jd = formula.julian_day(self.d.year, self.d.month, self.d.day, self.tz)
		ds = formula.decl_sun(jd)
		transit = formula.zuhr(self.lng, self.tz, formula.eq_time(jd))
		lat = self.lat
		return Times(tuple(i + adj for i,adj in zip(
			(
			formula.fajr   (transit, lat, ds, self.fajr_angle),
			formula.sunrise(transit, lat, ds, self.h),
			transit,
			formula.asr    (transit, lat, ds, self.asr_ratio),
			formula.maghrib(transit, lat, ds, self.h),
			formula.isha   (transit, lat, ds, self.isha_angle)),
			self.adjustments)))


class Times(object):

	def __init__(self, times):
		self.times = times
		self.use_second = False

	def get_time(self, i):
		if self.use_second: return datetime.time(*self.get_hms(i))
		else: return datetime.time(*self.get_hm(i))

	def get_hms(self, i):
		seconds = int(math.ceil(self.times[i] * 3600))
		h, seconds = divmod(seconds, 3600)
		m, seconds = divmod(seconds,   60)
		return (h, m, seconds)
	
	def get_hm(self, i):
		minutes = int(math.ceil(self.times[i] * 60))
		h, minutes = divmod(minutes, 60)
		return (h, minutes)
	
	def __iter__(self):
		return iter(self.get_time(i) for i in range(len(self.times)))

	_names = ('fajr', 'sunrise', 'zuhr', 'asr', 'maghrib', 'isha')
	def __getattr__(self, name):
		if name in self._names:
			return self.get_time(self._names.index(name))
		else:
			raise AttributeError("'{}' object has no attribute '{}'".
				format(self.__class__.__name__, name))
