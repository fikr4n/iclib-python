from iclib import salat
import datetime as dt


date = dt.date.today()
print('Date:', date)
print()

def _egypt_init():
	c = salat.TimeCalculator().date(date) \
		.location(-6.38043079, 106.85337984, 0, 7) \
		.method('egypt')
	return date, c.calculate()

def egypt_gettime():
	date, t = _egypt_init()
	for  i in (salat.FAJR, salat.SUNRISE, salat.ZUHR, salat.ASR,
			salat.MAGHRIB, salat.ISHA):
		print(t.get_time(i).strftime('%H:%M'))

def egypt_property_withsec():
	date, t = _egypt_init()
	t.use_second = True
	print(t.fajr)
	print(t.sunrise)
	print(t.zuhr)
	print(t.asr)
	print(t.maghrib)
	print(t.isha)

def egypt_iter_noadjust():
	c = salat.TimeCalculator().date(date) \
		.location(-6.38043079, 106.85337984, 0, 7) \
		.method('egypt', None, {})
	t = c.calculate()
	for i in t:
		print(i)

def muhammadiyah():
	c = salat.TimeCalculator().date(date) \
		.location(-6.38043079, 106.85337984, 0, 7) \
		.method('muhammadiyah')
	for i in c.calculate():
		print(i)

def mwl_noadjust():
	c = salat.TimeCalculator().date(date) \
		.location(-6.38043079, 106.85337984, 0, 7) \
		.method('mwl', 'majority', {})
	for i in c.calculate():
		print(i)

def mwl_hanafi_noadjust():
	c = salat.TimeCalculator().date(date) \
		.location(-6.38043079, 106.85337984, 0, 7) \
		.method('mwl', 'hanafi', {})
	for i in c.calculate():
		print(i)

def mwl_noadjust_100m():
	c = salat.TimeCalculator().date(date) \
		.location(-6.38043079, 106.85337984, 100, 7) \
		.method('mwl', 'majority', {})
	for i in c.calculate():
		print(i)

def mwl_1jan2015():
	c = salat.TimeCalculator().gregorian_date(2015, 1, 1) \
		.location(-6.38043079, 106.85337984, 0, 7) \
		.method('mwl')
	for i in c.calculate():
		print(i)

def mwl_1jan2015_tomorrow():
	c = salat.TimeCalculator().gregorian_date(2015, 1, 1) \
		.location(-6.38043079, 106.85337984, 0, 7) \
		.method('mwl')
	c.date_relative(+1)
	for i in c.calculate():
		print(i)


loc = sorted(locals().items())
for k,v in loc:
	if not k.startswith('_') and callable(v):
		print('-' * 5, k, '-' * 5)
		v()
		print()
