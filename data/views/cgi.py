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

# -------------------------------------------------------------------
# SEARCH
# -------------------------------------------------------------------

@login_required
def search(request):
        search  = request.GET.get('term') or request.POST.get('term')
        list2   = []
	"""
	qs	= Bookmark.objects.filter(name__iregex=search) | Bookmark.objects.filter(user__iregex=search)
	for q in qs[:10]:
                        list2.append({
                               	"label": q.name,
 	                       	"value": "/gamma/folder/%d/?search=%s" % (q.folder.id,q.id),
                               	"category": q.folder.name,
                      	})
	"""
	return render_json(request,list2)
