import re
from django import template
register 	= template.Library()

def toJavascriptDate(mydate):
	try: 	return "new Date(%d,%d,%d,%d,%d,%d)" % ( mydate.year, mydate.month-1, mydate.day, mydate.hour, mydate.minute, mydate.day )
	except: 
		try: 	return "new Date(%d,%d,%d)" % ( mydate.year, mydate.month-1, mydate.day )
		except: return "new Date()"

def toFormatedDate(mydate):
	try:
		return "%d-%d-%d" % ( mydate.year, mydate.month, mydate.day )
	except:
		return ""

def toYearMonth(mydate):
	try:
		return mydate.strftime("%Y %b")
	except:
		return ""

register.filter('newjsdate', 	toJavascriptDate)
register.filter('formatdate', 	toFormatedDate)
register.filter('yearmonth', 	toYearMonth)

