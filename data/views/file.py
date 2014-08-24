from __future__ import division
from django.contrib.auth.decorators     import login_required, permission_required
from django.contrib.auth.models         import User
from django.core.paginator              import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models                import modelformset_factory
from django.contrib                     import messages
from django.forms                       import ModelForm
from django.http                        import HttpResponseRedirect, HttpResponse
from django.conf                        import settings
from data.models 			import *
from datetime                           import datetime, timedelta
from django                             import forms
from libs.shared 			import * 
import numpy
import json
import sys
import re

@login_required
def get(request,type,id):
	return render(request,"data/templates/form.html",locals())

@login_required
def upload(request,id):
	return render(request,"data/templates/form.html",locals())
