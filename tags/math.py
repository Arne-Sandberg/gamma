import re
from django import template
register = template.Library()

def substract(a,b):
	return a-b

def sci_notation(a):
	if a<0.01:
		return 0
	else:
		return a 

def multiply(a,b):
	return float(a)*float(b)

def myrange(i,j):
	return range(i,j)

def absolute(i):
	if i<0:
		return -1 * i
	else:
		return i

register.filter('substract', 		substract)
register.filter('absolute', 		absolute)
register.filter('myrange', 		myrange)
register.filter('multiply', 		multiply)
register.filter('sci_notation', 	sci_notation)
