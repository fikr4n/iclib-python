# Copyright (C) 2015 Fikrul Arif
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Prayer times calculator"""

from . import formula
from .util import hms, hm
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
		"""Set method and adjustment of calculation

		Standard angle names for param angle are available in STANDARD_ANGLES.
		Value for asr_ratio can be 'hanafi' or anything else (default value),
		such as 'majority' or None, which means majority of scholars except
		Imam Hanafi. Adjustment is addition to the result, use ZUHR, ASR, etc as
		the key. By default it adjusts Zuhr time by 2 minutes to wait the Sun
		turn down to the west.

		Param:
		angle as str or 2-tuple of number - Fajr and Isha angle
		asr_ratio - ratio of object's shadow to determine Asr time
		adjustment as dict of int to number - result adjustment

		Return:
		self for chaining
		"""
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
		"""Set the location

		Param:
		lat as number - latitude in degrees
		lng as number - longitude in degrees
		h as number - altitude/height of the place in meters
		tz as number - timezone in hours, x means UTC+x

		Return:
		self for chaining
		"""
		self.lat = lat
		self.lng = lng
		self.h = h
		if isinstance(tz, datetime.tzinfo):
			self.tz = tz.utcoffset(None).total_seconds() / 3600.0
		else:
			self.tz = tz
		return self

	def date(self, date):
		"""Set the date

		Param:
		date as datetime.date

		Return:
		self for chaining
		"""
		self.jd = formula.gregorian_to_jd(date.year, date.month, date.day)
		return self

	def gregorian_date(self, y, m, d):
		"""Set the date, like method date(self, date)
		
		Param:
		y as int - year
		m as int - month [1..12]
		d as int - day of month [1..31]

		Return:
		self for chaining
		"""
		self.jd = formula.gregorian_to_jd(y, m, d)
		return self

	def date_relative(self, days):
		"""Add the date by days"""
		self.jd += days
		return self

	def calculate(self):
		"""Calculate the prayer times
		
		This method can be called several times. For example, you set the date
		and call this method, update the date to tomorrow and call this method.

		Return:
		result as Times
		"""
		# julian day of local midday (minus timezone, plus 12 hours)
		jd = formula.adjust_jd_hour(self.jd, -self.tz + 12)
		ds = formula.decl_sun(jd)
		transit = formula.zuhr(self.lng, self.tz, formula.eq_time(jd))
		lat = self.lat
		return Times([i + adj for i,adj in zip(
			(
			formula.fajr   (transit, lat, ds, self.fajr_angle),
			formula.sunrise(transit, lat, ds, self.h),
			transit,
			formula.asr    (transit, lat, ds, self.asr_ratio),
			formula.maghrib(transit, lat, ds, self.h),
			formula.isha   (transit, lat, ds, self.isha_angle)),
			self.adjustments)])

inf = float('inf')

class Times(object):
	"""Result of TimeCalculator"""

	def __init__(self, times):
		self.times = times
		self.use_second = False
		if times[SUNRISE] == -inf or times[MAGHRIB] == inf:
			times[ZUHR] = inf
			times[ASR] = inf

	def get_time(self, i):
		"""Return the time as datetime.time

		The value of self.use_second is considered.

		Param:
		i as int - ZUHR, ASR, etc
		"""
		# negative hours will raise exception
		try:
			if self.use_second: return datetime.time(*self.get_hms(i))
			else: return datetime.time(*self.get_hm(i))
		except TypeError:
			return None

	def get_hms(self, i):
		"""Return the time as 3-tuple of hour-minute-second

		Param:
		i as int - ZUHR, ASR, etc
		"""
		return hms(self.times[i])
	
	def get_hm(self, i):
		"""Return the time as 2-tuple of hour-minute

		Param:
		i as int - ZUHR, ASR, etc
		"""
		return hm(self.times[i])
	
	def __iter__(self):
		return iter(self.get_time(i) for i in range(len(self.times)))

	_names = ('fajr', 'sunrise', 'zuhr', 'asr', 'maghrib', 'isha')
	def __getattr__(self, name):
		if name in self._names:
			return self.get_time(self._names.index(name))
		else:
			raise AttributeError("'{}' object has no attribute '{}'".
				format(self.__class__.__name__, name))
