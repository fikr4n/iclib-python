# -*- coding: utf-8 -*-
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
import math


def dms(deg):
	"""Convert degree to degree-minute-second

	If deg is negative, all values of tuple are negative or 0.
	"""
	seconds = deg * 3600
	d = seconds / 3600
	m = math.fmod(seconds, 3600) / 60
	s = math.fmod(seconds, 60)
	return (int(d), int(m), s)

def dms_str(deg, prec):
	d, m, s = dms(deg)
	if deg < 0:
		return '-{}° {}′ {:.{}f}″'.format(-d, -m, -s, prec)
	else:
		return '{}° {}′ {:.{}f}″'.format(d, m, s, prec)

def hms(hours):
	"""Convert hours to hour-minute-second

	If hours is negative, only hour of the tuple is negative.
	"""
	if math.isinf(hours):
		return None
	seconds = int(math.ceil(hours * 3600))
	h, seconds = divmod(seconds, 3600)
	m, seconds = divmod(seconds,   60)
	return (h, m, seconds)

def hm(hours):
	"""Convert hours to hour-minute

	If hours is negative, only hour of the tuple is negative.
	"""
	if math.isinf(hours):
		return None
	minutes = int(math.ceil(hours * 60))
	h, minutes = divmod(minutes, 60)
	return (h, minutes)

