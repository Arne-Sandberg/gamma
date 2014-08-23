from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import messages
from django.contrib import auth
from libs.shared import *

# --------------------------------------------
# REDIRECT.-
# --------------------------------------------
@login_required
def redirect(request):
	jsondata = {}
	# jsondata['request'] = request.GET;
	# PARSE ARGUMENTS.-
	ARGS = []
	for j in request.GET:
		key = j
		val = request.GET.get(j)
		if not key:				pass
		elif key == "amp":			pass
		elif key == "amp;":			pass
		elif key == "csrfmiddlewaretoken": 	pass
		else:
			arg = { "key":key, "val":val, } 
			ARGS.append(arg)
	# FORM URL STRING.-
	arr = []
	for arg in ARGS:
		arr.append( "%s=%s" % ( unicode(arg['key']), unicode(arg['val'])) )
	url = '&'.join(arr)
	jsondata['url'] = url
	# RETURN JSON.-
	return render_json(request,jsondata)

# --------------------------------------------
# PRINT HOME
# --------------------------------------------
def home(request):
        return render(request,"templates/home.html", locals())
