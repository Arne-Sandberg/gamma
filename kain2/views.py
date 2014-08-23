from __future__ import division
from django.contrib.auth.decorators     import login_required, permission_required
from django.contrib.auth.models         import User
from django.core.paginator              import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models                import modelformset_factory
from django.contrib                     import messages
from django.forms                       import ModelForm
from django.http                        import HttpResponseRedirect, HttpResponse
from django.conf                        import settings
from kain2.models 			import *
from datetime                           import datetime, timedelta
from django                             import forms
from libs.shared 			import * 
import numpy
import json
import sys
import re

# -------------------------------------------------------------------
# CGI 
# -------------------------------------------------------------------

@login_required
@permission_required('admin.kaizen')
def cgi_search(request):
        search  = request.GET.get('term') or request.POST.get('term')
        list2   = []
	qs	= Bookmark.objects.filter(name__iregex=search) | Bookmark.objects.filter(user__iregex=search)
	for q in qs[:10]:
                        list2.append({
                               	"label": q.name,
 	                       	"value": "/kain/folder/%d/?search=%s" % (q.folder.id,q.id),
                               	"category": q.folder.name,
                      	})
	return render_json(request,list2)

@login_required
@permission_required('admin.kaizen')
def cgi_name(request,id):
        jsondata = {}
	val = request.GET.get('name')
	if not val:
		jsondata['message'] = "Missing value"
		jsondata['status']  = 0 
	elif Bookmark.exists(id):
		bk = Bookmark.objects.get(id=id)
		bk.name = val
		bk.save()
		jsondata['status']  = 1 
	else:
		jsondata['message'] = "No bookmark with such ID"
		jsondata['status']  = 0 
        return render_json(request,jsondata)

@login_required
@permission_required('admin.kaizen')
def cgi_url(request,id):
        jsondata = {}
	val = request.GET.get('url')
	if not val:
		jsondata['message'] = "Missing value"
		jsondata['status']  = 0 
	elif Bookmark.exists(id):
		bk = Bookmark.objects.get(id=id)
		bk.url = val
		bk.save()
		jsondata['status']  = 1 
	else:
		jsondata['message'] = "No bookmark with such ID"
		jsondata['status']  = 0 
        return render_json(request,jsondata)

@login_required
@permission_required('admin.kaizen')
def cgi_user(request,id):
        jsondata = {}
	val = request.GET.get('user') or "" 
	if Bookmark.exists(id):
		bk = Bookmark.objects.get(id=id)
		bk.user = val
		bk.save()
		jsondata['status']  = 1 
	else:
		jsondata['message'] = "No bookmark with such ID"
		jsondata['status']  = 0 
        return render_json(request,jsondata)

@login_required
@permission_required('admin.kaizen')
def cgi_pass(request,id):
        jsondata = {}
	val = request.GET.get('pass') or ""
	if Bookmark.exists(id):
		bk = Bookmark.objects.get(id=id)
		bk.password = val
		bk.save()
		jsondata['status']  = 1 
	else:
		jsondata['message'] = "No bookmark with such ID"
		jsondata['status']  = 0 
        return render_json(request,jsondata)

@login_required
@permission_required('admin.kaizen')
def cgi_add(request):
        jsondata = {}
	name = request.GET.get('name')
	fid  = request.GET.get('fid')
	if not KainFolder.exists(fid):
		jsondata['message'] = "No folder with such ID"
		jsondata['status']  = 0 
	elif not Bookmark.exists(name):
		f  = KainFolder.objects.get(id=fid)
		bk = Bookmark()
		bk.folder = f 
		bk.name = name
		bk.save()
		jsondata['status']  = 1 
		jsondata['gid']     = bk.id
	else:
		jsondata['message'] = "bookmark with such name already exists"
		jsondata['status']  = 0 
        return render_json(request,jsondata)

@login_required
@permission_required('admin.kaizen')
def cgi_delete(request,id):
        jsondata = {}
	if Bookmark.exists(id):
		bk = Bookmark.objects.get(id=id)
		bk.delete()
		jsondata['status']  = 1 
	else:
		jsondata['message'] = "No bookmark with such ID"
		jsondata['status']  = 0 
        return render_json(request,jsondata)

# -------------------------------------------------------------------
# VIEW 
# -------------------------------------------------------------------

@login_required
@permission_required('admin.kaizen')
def root(request):
	table = KainFolder.objects.all().order_by('name')
	page = request.GET.get('page') or 1
	pageobj = Paginator(table,15,orphans=5).page(page)
	return render(request,"kain2/templates/root.html",locals())

@login_required
@permission_required('admin.kaizen')
def folder(request,id):
	search = request.GET.get('search') or None
	if KainFolder.exists(id):
		table = KainFolder.objects.get(id=id)
		if search:
			children = Bookmark.objects.filter(folder=table,id=search)
		else:
			children = table.children()
		children = children.order_by('name')
		page = request.GET.get('page') or 1
		pageobj = Paginator(children,10,orphans=10).page(page)
	else:
		messages.add_message(request, messages.ERROR, "No folder found")
	return render(request,"kain2/templates/folder.html",locals())

# -------------------------------------------------------------------
# CONTROLLER 
# -------------------------------------------------------------------

@login_required
@permission_required('admin.kaizen')
def add(request):
	myform = getform(KainFolder)
        req, non = getfields(KainFolder)
	f = KainFolder()
	if request.POST:
		form = myform(request.POST,instance=f)
		for field in non: form.fields[field].required = False
		if not form.is_valid():
                	return render(request,"kain2/templates/form.html",locals())
		else:
			f.save()
			messages.add_message(request, messages.SUCCESS, "Saved!")
                	return HttpResponseRedirect("/kain/folder/%d/"%f.id)
	else:
		form = myform()
	return render(request,"kain2/templates/form.html",locals())

@login_required
@permission_required('admin.kaizen')
def edit(request,id):
	myform = getform(KainFolder)
        req, non = getfields(KainFolder)
	if KainFolder.exists(id):
		f = KainFolder.objects.get(id=id)
	else:
		messages.add_message(request, messages.ERROR,"Element does not exist")
                return HttpResponseRedirect("#")
	if request.POST:
		form = myform(request.POST,instance=f)
		for field in non: form.fields[field].required = False
		if not form.is_valid():
                	return render(request,"kain2/templates/form.html",locals())
		else:
			f.save()
			messages.add_message(request, messages.SUCCESS, "Saved!")
                	return HttpResponseRedirect("/kain/folder/%d/"%f.id)
	else:
		form = myform(instance=f)
	return render(request,"kain2/templates/form.html",locals())

@login_required
@permission_required('admin.kaizen')
def delete(request,id):
	if KainFolder.exists(id):
		KainFolder.objects.get(id=id).delete()
                messages.add_message(request, messages.WARNING, "Element deleted!")
	else:
		messages.add_message(request, messages.ERROR,"Element does not exist")
  	return HttpResponseRedirect("/kain/root/")

