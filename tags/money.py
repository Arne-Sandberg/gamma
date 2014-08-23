import re
from django import template
register = template.Library()

def toMoney(value):
	if not value:		return "$0.00"
	elif value >= 0:	return "$%.2f" % float(value)
	else:			return "($%.2f)" % float(value*-1)

def toProportion(value):
	if not value:		return "0.00%"
	else:			return "%.2f%s" % ( float(value), "%" )

def toAmount(value):
	if not value:		return "0u"
	else:			return "%d%s" % ( int(value), "u" )

register.filter('amount', 	toAmount)
register.filter('money', 	toMoney)
register.filter('prop', 	toProportion)
