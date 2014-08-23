import re
from django import template
register = template.Library()

def print_ascii(string):
	try: 
		s = string 
		s = re.sub(r'\xf3','',s)
		return s
	except:
		return '_'

register.filter('ascii', print_ascii)
