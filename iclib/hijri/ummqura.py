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
"""Convert date to Umm al-Qura calendar and vice versa"""

from .. import formula


def from_gregorian(y, m, d):
	"""Convert from Gregorian date

	This is valid only for 1420-1450 AH (April 17 1999 - May 14 2029).

	Param:
	y as int - year
	m as int - month [1..12]
	d as int - day of month [1..31]

	Return:
	int - year
	int - month [1..12]
	int - day of month [1..30]
	int - number of days in the Hijri month
	"""
	# valid from 1420 AH (1999-04-17 CE) to 1450 AH (2029-05-14 CE)
	jd = int(formula.gregorian_to_jd(y, m, d) + 0.5) # jd midday
	accu = 2451286 # jd of 1999-04-17 midday
	i = -1
	while accu <= jd:
		i += 1
		accu += _month_len[i] + 29
	if i == -1: raise IndexError(i)
	month_start = accu - _month_len[i] - 29
	# here i is index where the month we're looking for is
	h_year = i // 12 + 1420
	h_month = i % 12 + 1
	h_day = jd - month_start + 1
	return (h_year, h_month, h_day, _month_len[i] + 29)

def to_gregorian(y, m, d):
	"""Convert to Gregorian date

	This is valid only for 1420-1450 AH (April 17 1999 - May 14 2029).

	Param:
	y as int - year
	m as int - month [1..12]
	d as int - day of month [1..30]

	Return:
	int - year
	int - month [1..12]
	int - day of month [1..31]
	"""
	index = (y - 1420) * 12 + m - 1
	if index < 0 or index > len(_month_len): raise IndexError(index)
	jd = 2451285.5 + sum(i + 29 for i in _month_len[:index]) + d - 1
	return formula.jd_to_gregorian(jd)

_month_len = (0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 
	0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 
	1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 
	1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 
	1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 
	1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 
	0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 
	0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 
	1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 
	0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 
	0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 
	0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 
	0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 
	1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 
	0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 
	1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 
	0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 
	1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 
	1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 
	1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 
	0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 
	1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 
	0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 
	1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 
	0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 
	0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 
	0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 
	1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 
	0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 
	0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 
	1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1)

