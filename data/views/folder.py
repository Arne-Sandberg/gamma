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
# ADD FOLDER
# -------------------------------------------------------------------
@login_required
def add(request):

	# BEGIN.-
        list2 = {}
	list2['status'] = True
	list2['message'] = ""

	# GET FATHER FOLDER.-
	father = Folder()
	fid = request.GET.get('fid') or 0
	if fid:
		father = Folder.objects.get(id=unicode(fid))

	# PERMISSIONS:
	# MUST BE A SUPER USER OR 
	# FATHER MUST HAVE WRITE PERMISSIONS.-
	if request.user.is_superuser:
		pass
	elif father.id and not father.write:
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# GET NAME.-
	name = request.GET.get('name') or None
	if not name:
		list2['status'] = False
		list2['message'] = "No hay nombre!"

	# CREATE FOLDER.-
	if list2['status']:
		folder = Folder()
		folder.name = name
		folder.read = False
		folder.write = False
		folder.user = request.user
		folder.date = datetime.now()
		if father and father.id:
			folder.father = father
			folder.read = father.read
			folder.write = father.write
		folder.save()
		list2['folder_id'] = folder.id
		list2['status'] = True

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# MOD FOLDER
# -------------------------------------------------------------------
@login_required
def mod(request):

	# BEGIN.-
        list2 = {}
	list2['status'] = True
	list2['message'] = ""

	# GET FOLDER.-
	folder = Folder()
	fid = request.GET.get('fid') or 0
	if fid:
		folder = Folder.objects.get(id=unicode(fid))
	else:
		list2['message'] = "La carpeta no existe"
		list2['status'] = False

	# PERMISSIONS:
	# MUST BE A SUPER USER OR 
	# I HAVE TO BE THE OWNER.-
	if request.user.is_superuser:
		pass
	elif folder.id and not request.user == folder.user: 
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# GET NAME.-
	name = request.GET.get('name') or None
	if not name:
		list2['status'] = False
		list2['message'] = "No hay nombre!"

	# UPDATE FOLDER.-
	if list2['status']:
		folder.name = name
		folder.save()
		list2['status'] = True

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# REM FOLDER
# -------------------------------------------------------------------
@login_required
def rem(request):

	# BEGIN.-
        list2 = {}
	list2['status'] = True
	list2['message'] = ""

	# GET FOLDER.-
	folder = Folder()
	fid = request.GET.get('fid') or 0
	if fid:
		folder = Folder.objects.get(id=unicode(fid))
	else:
		list2['message'] = "La carpeta no existe"
		list2['status'] = False

	# PERMISSIONS:
	# MUST BE A SUPER USER OR 
	# I HAVE TO BE THE OWNER.-
	if request.user.is_superuser:
		pass
	elif folder.id and not request.user == folder.user: 
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# DELETE FOLDER.-
	if list2['status']:
		folder.delete()
		list2['status'] = True

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# SWITCH READ 
# -------------------------------------------------------------------
@login_required
def read(request):

	# BEGIN.-
        list2 = {}
	list2['status'] = True
	list2['message'] = ""

	# GET FOLDER.-
	folder = Folder()
	fid = request.GET.get('fid') or 0
	if fid:
		folder = Folder.objects.get(id=unicode(fid))
	else:
		list2['message'] = "La carpeta no existe"
		list2['status'] = False

	# PERMISSIONS:
	# MUST BE A SUPER USER OR 
	# I HAVE TO BE THE OWNER.-
	if request.user.is_superuser:
		pass
	elif folder.id and not request.user == folder.user: 
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# SWITCH PERMISSIONS.-
	if list2['status']:
		folder.setRead(not folder.read)
		list2['status'] = True

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# SWITCH WRITE
# -------------------------------------------------------------------
@login_required
def write(request):

	# BEGIN.-
        list2 = {}
	list2['status'] = True
	list2['message'] = ""

	# GET FOLDER.-
	folder = Folder()
	fid = request.GET.get('fid') or 0
	if fid:
		folder = Folder.objects.get(id=unicode(fid))
	else:
		list2['message'] = "La carpeta no existe"
		list2['status'] = False

	# PERMISSIONS:
	# MUST BE A SUPER USER OR 
	# I HAVE TO BE THE OWNER.-
	if request.user.is_superuser:
		pass
	elif folder.id and not request.user == folder.user: 
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# SWITCH PERMISSIONS.-
	if list2['status']:
		folder.setWrite(not folder.write)
		list2['status'] = True

	# END 
	return render_json(request,list2)
