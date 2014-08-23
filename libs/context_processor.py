# -*- coding: utf8 -*- 
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from random import choice
import json
import sys

def render_error(request,message,data=None):
	data['message'] = message
	return render(render,"templates/error/exception.html",data)

def render(request,template,data=None):
	data['messages'] 	= messages.get_messages(request);
	return render_to_response(
				template, 
				data,
                              	context_instance=RequestContext(request)
			)

def render_json(request,data):
	jsondata = ""
	try: 
		jsondata = json.dumps(data)
	except Exception, e:
		messages.add_message(request, messages.ERROR, "Can't dump data to JSON: "+unicode(e))
	return HttpResponse(jsondata)
