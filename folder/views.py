from __future__ import division
from django.contrib.auth.decorators     import login_required, permission_required
from django.contrib.auth.models         import User
from django.core.paginator              import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models                import modelformset_factory
from django.contrib                     import messages
from django.forms                       import ModelForm
from django.http                        import HttpResponseRedirect, HttpResponse
from django.conf                        import settings
from folder.models 			import *
from datetime                           import datetime, timedelta
from django                             import forms
from libs.shared 			import * 
import random
import numpy
import json
import sys
import re
import os

# -------------------------------------------------------------------
# CGI ADD FOLDER
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

	# PERMISSIONS MUST BE A SUPER USER
	if request.user.is_superuser:
		pass
	else:
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
		messages.add_message(request, messages.SUCCESS, "Carpeta creada!")

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# CGI MOD FOLDER
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

	# PERMISSIONS MUST BE A SUPER USER OR 
	if request.user.is_superuser:
		pass
	else:
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
		messages.add_message(request, messages.SUCCESS, "Carpeta actualizada!")

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# CGI REM FOLDER
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

	# PERMISSIONS: ONLY SUPERUSER
	if request.user.is_superuser:
		pass
	else:
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# DELETE FOLDER.-
	if list2['status']:
		folder.delete()
		list2['status'] = True
		messages.add_message(request, messages.WARNING, "Carpeta eliminada!")

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# CGI SWITCH READ 
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

	# PERMISSIONS: ONLY SUPERUSER
	if request.user.is_superuser:
		pass
	else:
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# SWITCH PERMISSIONS.-
	if list2['status']:
		folder.setRead(not folder.read)
		list2['status'] = True
		messages.add_message(request, messages.WARNING, "Permisos actualizados!")

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# CGI SWITCH WRITE
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

	# PERMISSIONS: ONLY SUPERUSER
	if request.user.is_superuser:
		pass
	else:
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# SWITCH PERMISSIONS.-
	if list2['status']:
		folder.setWrite(not folder.write)
		list2['status'] = True
		messages.add_message(request, messages.WARNING, "Permisos actualizados!")

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# VIEW FOLDER
# -------------------------------------------------------------------
@login_required
def folder(request,fid=None):

	# GET FOLDER OR NONE.-
	if fid:
		if Folder.existsID(fid):
			MYFOLDER = Folder.objects.get(id=fid)
		else:
	                messages.add_message(request, messages.ERROR, "No existe esta carpeta!")
			return HttpResponseRedirect("/folder/")
	else:
		MYFOLDER = None
	fid = None;

	# PERMISSIONS.
	# IT MUST BE A SUPERUSER OR A PUBLIC FOLDER.-
	if request.user.is_superuser:
		pass
	elif MYFOLDER and MYFOLDER.id and not MYFOLDER.read:
	       	messages.add_message(request, messages.ERROR, "Prohibido!")
		return render(request,"folder/templates/folder.html",locals())

	# GET SUBFOLDERS.-
	if MYFOLDER:
		subfolders = MYFOLDER.children(request.user)
	elif request.user.is_superuser:
		subfolders = Folder.objects.filter(father=None)
	else:
		subfolders = Folder.objects.filter(father=None,read=True)

	# GET FILES.-
	if MYFOLDER:
		qs 	= MYFOLDER.files()
		page 	= request.GET.get('page') or 1
		pageobj = Paginator(qs,30,orphans=5).page(page)
		qs 	= None

	# END 
	return render(request,"folder/templates/folder.html",locals())

# -------------------------------------------------------------------
# COMPRESS
# -------------------------------------------------------------------
@login_required
def compress(request):

	# BEGIN
	list2 = {}
	list2['status'] = True

	# GET FOLDER.-
	fid = request.GET.get('fid') or 0
	if fid:
		folder = Folder.objects.get(id=unicode(fid))
	else:
		list2['message'] = "La carpeta no existe"
		list2['status'] = False

	# PERMISSIONS.
	# IT MUST BE A SUPERUSER.-
	if request.user.is_superuser:
		pass
	else:
	       	messages.add_message(request, messages.ERROR, "Prohibido!")
		return render(request,"folder/templates/folder.html",locals())

	# COMPRESS
	if list2['status']:
		ts1 = random.randint(100000000,900000000)
		ts2 = random.randint(100000000,900000000)
		src  = "tmp/%d.zip" % ts1
		name = "%s/%s" % (settings.MEDIA_ROOT,src)
		os.system("rm -rf %s/tmp/*" % settings.MEDIA_ROOT)
		os.system("cd %s; zip -r %s -P '%d' %s " % (settings.MEDIA_ROOT,name,ts2,folder.short_path()))
		list2['src'] = src
		list2['pass'] = ts2

	# END 
	return render_json(request,list2)
