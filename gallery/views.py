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
	url = "/gallery/%d/?playlistID=%d" % (qs[0].id,MYFOLDER.id)
	return HttpResponseRedirect(url)

# -------------------------------------------------------------------
# LOAD THE FOLLOWING ELEMENTS OF THE PLAYLIST
# -------------------------------------------------------------------
@login_required
def fetch(request):

	# BEGIN
	list2 = {}
	MYFOLDER = None
	MYFILE	 = None
	MYCURSOR = None
	list2['status'] = True
	list2['message'] = ""
	list2['cacheNext'] = []
	list2['cachePrevious'] = []

	# GET CURSOR POSITION.-
	cursorID = (int)(request.GET.get('cursorID') or 0)
	MYCURSOR = cursorID
	
	# GET PLAYLIST.-
	playlistID = (int)(request.GET.get('playlistID') or 0)
	if playlistID: 
		if Folder.existsID(playlistID):
			MYFOLDER = Folder.objects.get(id=playlistID)
		else:
			list2['status'] = False
			list2['message'] = "No existe la lista de reproduccion"
			return render_json(request,list2)
	else:
		list2['status'] = False
		list2['message'] = "Faltan parametros"
		return render_json(request,list2)

	# PERMISSIONS.
	# IT MUST BE A SUPERUSER OR A PUBLIC FOLDER.-
	if request.user.is_superuser:
		pass
	elif MYFOLDER and MYFOLDER.id and not MYFOLDER.read:
		list2['status'] = False
		list2['message'] = "No se puede leer la lista de reproduccion"
		return render_json(request,list2)

	# GET PLAYLIST 
	playlist = MYFOLDER.playlist(request.user)
	if playlist.count()<1:
		list2['emptyList'] = True
		return render_json(request,list2)

	# IF RANDOM LIST.-
	isRandom = (int)(request.GET.get('random')  or 0)
	if isRandom:
		for i in range(0,settings.PLAYLIST_FETCH_CACHE):
			q = random.randint(0,playlist.count())
			list2['cacheNext'].append(playlist[q].serialize())

	# IF NOT RANDOM.-
	else:

		# GET NEXT.-
		fetchNext = (int)(request.GET.get('fetchNext') or 0)
		if fetchNext:
			q = MYCURSOR + 1
			for i in range(0,settings.PLAYLIST_FETCH_CACHE):
				if q >= playlist.count():
					q = 0
				list2['cacheNext'].append(playlist[q].serialize())
				q += 1

		# GET PREVIOUS.-
		fetchPrevious = (int)(request.GET.get('fetchPrevious') or 0)
		if fetchPrevious:
			q = MYCURSOR - 1
			for i in range(0,settings.PLAYLIST_FETCH_CACHE):
				if q<1:
					q = playlist.count()-1
				list2['cachePrevious'].insert(0,playlist[q].serialize())
				q -= 1

		# END 
		return render_json(request,list2)

# -------------------------------------------------------------------
# VIEW GALLERY
# EVERYTHING IS HANDLED OVER JAVASCRIPT TOGETHER WITH 
# OTHER VIEWS. THIS ONLY SERVES THE TEMPLATE.-
# -------------------------------------------------------------------
@login_required
def gallery(request,fid):
	playlistID = request.GET.get('playlistId')
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

# -------------------------------------------------------------------
# FETCH ONLY ONE.-
# -------------------------------------------------------------------
@login_required
def get(request,fileID):

	# BEGIN
	list2 = {}
	list2['status'] = True
	list2['message'] = ""
	list2['file'] = []

	# GET FILE.-
	if GFile.existsID(fileID):
		MYFILE = GFile.objects.get(id=fileID)
	else:
		list2['status'] = False
		list2['message'] = "No existe el archivo"
		return render_json(request,list2)

	# GET PLAYLIST OR FOLDER ID
	playlistID = (int)(request.GET.get('playlistID') or 0)
	if playlistID: 
		list2['playlistID'] = playlistID
		if Folder.existsID(playlistID):
			MYFOLDER = Folder.objects.get(id=playlistID)
		else:
			list2['status'] = False
			list2['message'] = "No existe la lista de reproduccion"
			return render_json(request,list2)
	else:
		list2['playlistID'] = MYFILE.folder.id
		MYFOLDER = MYFILE.folder

	# PERMISSIONS.
	# IT MUST BE A SUPERUSER OR A PUBLIC FOLDER.-
	if request.user.is_superuser:
		pass
	elif MYFOLDER and MYFOLDER.id and not MYFOLDER.read:
		list2['status'] = False
		list2['message'] = "No se puede leer la lista de reproduccion"
		return render_json(request,list2)

	# GET PLAYLIST AND CURSOR
	playlist = MYFOLDER.playlist(request.user)
	list2['playlistID'] = MYFOLDER.id
	list2['playlistCount'] = playlist.count()
	i = 0
	while i<playlist.count() and playlist[i]!= MYFILE:
		i += 1
	MYCURSOR = i
	list2['cursorID'] = MYCURSOR

	# RETURN FILE.-
	list2['file'] = MYFILE.serialize()
	list2['cache_size']  = settings.PLAYLIST_FETCH_CACHE
	list2['cache_fetch'] = settings.PLAYLIST_NEXT_FETCH
	return render_json(request,list2)

