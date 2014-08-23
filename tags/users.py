import re
from django import template
from ..models import UserSSJ2
register = template.Library()

def filename(name):
	return name.split('/')[-1]

register.filter('fname',	filename)
