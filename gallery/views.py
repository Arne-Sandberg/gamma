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
import numpy
import json
import sys
import re

# -------------------------------------------------------------------
# START PLAYLIST BY A GIVEN FOLDER.-
# -------------------------------------------------------------------
@login_required
def playlist(request,fid):

	# GET FOLDER.-
	if Folder.existsID(fid):
		MYFOLDER = Folder.objects.get(id=fid)
	else:
		messages.add_message(request, messages.ERROR, "No existe esta carpeta!")
		return HttpResponseRedirect("/folder/")

	# PERMISSIONS.
	# IT MUST BE A SUPERUSER OR A PUBLIC FOLDER OR OWNER.-
	if request.user.is_superuser:
		pass
	elif MYFOLDER and MYFOLDER.id and not MYFOLDER.read:
	       	messages.add_message(request, messages.ERROR, "Prohibido!")
		return HttpResponseRedirect("/folder/")

	# GET PLAYLIST.-
	qs = MYFOLDER.playlist(request.user)
	if not qs.count():
		messages.add_message(request, messages.ERROR, "No hay nada para reproducir!")
		return HttpResponseRedirect("/folder/%d/" % MYFOLDER.id)

	# REDIRECT TO FIRST ELEMENT OF PLAYLIST
	url = "/gallery/%d/?playlist=%d" % (qs[0].id,MYFOLDER.id)
	return HttpResponseRedirect(url)

# -------------------------------------------------------------------
# LOAD THE FOLLOWING ELEMENTS OF THE PLAYLIST
# -------------------------------------------------------------------
@login_required
def fetch(request,playlistID,cursorID):

	# BEGIN
	list2 = {}
	list2['status'] = True
	list2['message'] = ""
	list2['cache'] = []
	
	# GET PLAYLIST
	if Folder.existsID(playlistID):
		MYFOLDER = Folder.objects.get(id=playlistID)
	else:
		list2['status'] = False
		list2['message'] = "No existe la lista de reproduccion"

	# PERMISSIONS.
	# IT MUST BE A SUPERUSER OR A PUBLIC FOLDER.-
	if request.user.is_superuser:
		pass
	elif MYFILE and MYFILE.id and not MYFILE.folder.read:
		list2['status'] = False
		list2['message'] = "No se puede leer la lista de reproduccion"

	# FETCH LIST.-
	if list2['status']:
		qs = MYFOLDER.playlist(request.user)
	
		# GET NEXT LINEAR.-
		i = 0	
		q = 0
		while i < settings.PLAYLIST_FETCH_CACHE:

			# SERIALIZE ELEMENT
			list2['cache'].append(qs[q].serialize())

			# NEXT.-
			i += 1	
			q += 1
			if q >= qs.count():
				q = 0
	
	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# VIEW GALLERY
# -------------------------------------------------------------------
@login_required
def gallery(request,fid):

	# GET FILE.-
	if GFile.existsID(fid):
		MYFILE = GFile.objects.get(id=fid)
	else:
		messages.add_message(request, messages.ERROR, "No existe el archivo!")
		return HttpResponseRedirect("/folder/")

	# PERMISSIONS.
	# IT MUST BE A SUPERUSER OR A PUBLIC FOLDER.-
	if request.user.is_superuser:
		pass
	elif not MYFILE.folder.read:
	       	messages.add_message(request, messages.ERROR, "Prohibido!")
		return HttpResponseRedirect("/folder/")

	# CHECK HIERARCHY OF THE PLAYLIST.-
	hierarchy = request.GET.get('playlist') or None
	if hierarchy:
		playlist = Folder.objects.get(id=unicode(hierarchy))
	else:
		playlist = MYFILE.folder
	qs = playlist.playlist(request.user)
	i = 0
	while i<qs.count() and qs[i]!=MYFILE:
		i += 1
	playlist_index=i	
	playlist = None
	qs = None

	# END 
	return render(request,"gallery/templates/gallery.html",locals())

# -------------------------------------------------------------------
# CGI MOD FILE
# -------------------------------------------------------------------
@login_required
def mod(request):

	# BEGIN.-
        list2 = {}
	list2['status'] = True
	list2['message'] = ""

	# GET FILE.-
	fid = request.GET.get('fid') or 0
	if fid:
		file = GFile.objects.get(id=unicode(fid))
	else:
		list2['message'] = "El archivo no existe"
		list2['status'] = False

	# PERMISSIONS:
	# MUST BE A SUPER USER 
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
		file.setName(name)
		file.save()
		list2['status'] = True
		messages.add_message(request, messages.SUCCESS,"Archivo actualizado!")

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# CGI REM FILE 
# -------------------------------------------------------------------
@login_required
def rem(request):

	# BEGIN.-
        list2 = {}
	list2['status'] = True
	list2['message'] = ""

	# GET FILE.-
	fid = request.GET.get('fid') or 0
	if fid:
		file = GFile.objects.get(id=unicode(fid))
	else:
		list2['message'] = "El archivo no existe"
		list2['status'] = False

	# PERMISSIONS: ONLY SUPERUSER
	if request.user.is_superuser:
		pass
	else:
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# DELETE FILE.-
	if list2['status']:
		file.delete()
		list2['status'] = True
		messages.add_message(request, messages.SUCCESS,"Archivo eliminado!")

	# END 
	return render_json(request,list2)

# -------------------------------------------------------------------
# CGI ADDFILE 
# -------------------------------------------------------------------
@login_required
def add(request):

	# BEGIN.-
        list2 = {}
	list2['status'] = True
	list2['message'] = ""

	# GET FATHER FOLDER.-
	fid = request.POST.get('fid') or 0
	if fid:
		folder = Folder.objects.get(id=unicode(fid))
	else:
		list2['message'] = "La carpeta no existe"
		list2['status'] = False

	# PERMISSIONS:
	# MUST BE A SUPER USER OR 
	# FATHER MUST HAVE WRITE PERMISSIONS.-
	if request.user.is_superuser:
		pass
	elif folder.id and not folder.write:
		list2['message'] = "Prohibido!"
		list2['status'] = False

	# GET FILE.-
	myfile = request.FILES.get('file') or None
	if not myfile:
		list2['status'] = False
		list2['message'] = "No hay archivos!"

	# CREATE FOLDER.-
	if list2['status']:

		# PRE SAVE.-
		file = GFile()
		file.user = request.user
		file.date = datetime.now()
		file.folder = folder
		file.file = myfile
		file.setName()	

		# CHECK SIZE 
		if file.checkSize():
			file.save()
			list2['file'] = folder.id
			list2['status'] = True
		else:
			file.remove()
			list2['message'] = "Archivo muy pesado!"
			list2['status'] = False

	# END 
	return render_json(request,list2)
