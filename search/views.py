from __future__ import division
from django.contrib.auth.decorators     import login_required, permission_required
from django.contrib.auth.models         import User
from django.core.paginator              import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models                import modelformset_factory
from django.db.models 			import Q, Sum, Avg
from django.contrib                     import messages
from django.forms                       import ModelForm
from django.http                        import HttpResponseRedirect, HttpResponse
from django.conf                        import settings
from datetime                           import datetime, timedelta
from django                             import forms
from libs.shared 			import *
from folder.models 			import *
import numpy
import json
import sys
import re

@login_required
@permission_required('admin.kaizen')
def search(request):

	# BEGIN
        search  = request.GET.get('term') or request.POST.get('term')
        list2   = []

	# SEARCH FOR FOLDERS .-
	if request.user.is_superuser:
        	qs = Folder.objects.filter(name__iregex=search).order_by('name')[:5]
	else:
        	qs = Folder.objects.filter(name__iregex=search,read=True).order_by('name')[:5]
        for q in qs:
                       	list2.append({
                               	"label": q.name,
                               	"value": "/folder/%s/" % q.id,
                               	"category": "Carpetas",
                       	})

	# SEARCH FOR .-
	if request.user.is_superuser:
        	qs = GFile.objects.filter(name__iregex=search).order_by('name')[:5]
	else:
        	qs = GFile.objects.filter(name__iregex=search,folder__read=True).order_by('name')[:5]
        for q in qs:
                       	list2.append({
                               	"label": q.name,
                               	"value": "/gallery/%s/" % q.id,
                               	"category": "Archivos",
                       	})

	# END.-
        return render_json(request,list2)
