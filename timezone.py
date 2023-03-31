from datetime import datetime
import datetime as dt
import pytz

defaultFmt = "%Y-%m-%d %H:%M:%S %Z%z"
timezones = {'London': 'UTC', 'Los Angeles': 'US/Pacific', 'Berlin': 'Europe/Berlin', 'New Delhi': 'Asia/Kolkata'}

def getTimeDif(zone,SysTZ="UTC"):
	zone = pytz.timezone(zone)
	time = datetime.now()
	time = time.replace(tzinfo=pytz.timezone(SysTZ)).astimezone(zone)
	time=time.strftime("%z")
	return "%s:%s"%(time[:3],time[3:])

def convertTo(time, zone=None, fmt=defaultFmt, place=None, SysTZ="UTC"):
	if zone == None:
		zone = timezones[place]
	if type(zone) == str:
		zone = pytz.timezone(zone)
	time = time.replace(tzinfo=pytz.timezone(SysTZ)).astimezone(zone)
	if fmt == None:
		time = (time.replace(tzinfo=None))
		return (time)
	else:
		time = zone.normalize(time).strftime(fmt)
		return time


def toUTC(time, zone, fmt=defaultFmt):
	if type(zone)==str:
		zone = pytz.timezone(zone)
	if type(time) == str:
		time = datetime.strptime(time, fmt)
	time = zone.localize(time, is_dst=None)
	time = time.astimezone(pytz.utc)
	if fmt == None:
		return time.replace(tzinfo=None)
	else:
		return pytz.timezone("UTC").normalize(time).strftime(defaultFmt)


def searchTZ(keyword=None):
	tzs = pytz.all_timezones
	if keyword == None:
		return tzs
	else:
		r = []
		for i in tzs:
			if keyword in i:
				r += [i]
		return r


def timeIn(zone, fmt=defaultFmt, SysTZ="UTC"):
	zone = pytz.timezone(zone)
	time = datetime.now()
	time = time.replace(tzinfo=pytz.timezone(SysTZ)).astimezone(zone)
	if fmt is None:
		time = (time.replace(tzinfo=None))
		return time
	time = zone.normalize(time).strftime(fmt)
	return time


def WeekName(date=None, zone="UTC"):
	if date == None:
		date = timeIn(zone, None)
	fday = date
	lday = date
	while (fday.weekday() > 0):
		fday = fday - dt.timedelta(days=1)
	while (lday.weekday() < 6):
		lday = lday + dt.timedelta(days=1)
	return ("%s - %s" % (fday.strftime('%d %B %y'), lday.strftime('%d %B %y')))


def weekNo(date=None, zone="UTC"):
	if date == None:
		date = timeIn(zone, None)
	week = date.isocalendar()
	if week[1] < 10:
		week = int("%s0%s" % (week[0], week[1]))
	else:
		week = int("%s%s" % (week[0], week[1]))
	return week


def daysFromWeek(weekNum=None, zone="UTC"):
	if weekNum == None:
		weekNum = weekNo(timeIn(zone, None))
	days = []
	days += [dt.datetime.strptime("%s 1" % (weekNum), "%Y%W %w").date()]
	for i in range(1, 7):
		days += [(dt.datetime.combine(days[i - 1], dt.datetime.min.time()) + dt.timedelta(days=1)).date()]
	return (days)
