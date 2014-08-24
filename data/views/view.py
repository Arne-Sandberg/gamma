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
# DISPLAY FOLDER
# -------------------------------------------------------------------
@login_required
def folder(request,fid=None):

	# GET FOLDER OR NONE.-
	if fid:
		if Folder.existsID(fid):
			MYFOLDER = Folder.objects.get(id=fid)
		else:
	                messages.add_message(request, messages.ERROR, "No existe esta carpeta!")
			return render(request,"data/templates/folder.html",locals())
	else:
		MYFOLDER = None
	fid = None;

	# PERMISSIONS.
	# IT MUST BE A SUPERUSER OR A PUBLIC FOLDER OR OWNER.-
	if request.user.is_superuser:
		pass
	elif MYFOLDER and MYFOLDER.id and MYFOLDER.user == request.user: 
		pass
	elif MYFOLDER and MYFOLDER.id and not MYFOLDER.read:
	       	messages.add_message(request, messages.ERROR, "Prohibido!")
		return render(request,"data/templates/folder.html",locals())
	else:
		pass

	# GET PAGED CHILDREN.-
	if MYFOLDER:
		qs = MYFOLDER.children(request.user)
	elif request.user.is_superuser:
		qs = Folder.objects.filter(father=None)
	else:
		qs = Folder.objects.filter(father=None,read=True)
	page 	= request.GET.get('page') or 1
	pageobj = Paginator(qs,15,orphans=5).page(page)
	qs 	= None

	# END 
	return render(request,"data/templates/folder.html",locals())

@login_required
def file(request,id):
	return render(request,"data/templates/file.html",locals())

@login_required
def gallery(request,type,id):
	return render(request,"data/templates/file.html",locals())
