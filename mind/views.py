from __future__ import division
from django.contrib.auth.decorators     import login_required, permission_required
from django.contrib.auth.models         import User
from django.core.paginator              import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models                import modelformset_factory
from django.contrib                     import messages
from django.forms                       import ModelForm
from django.http                        import HttpResponseRedirect, HttpResponse
from django.conf                        import settings
from mind.models 			import *
from datetime                           import datetime, timedelta
from django                             import forms
from libs.shared 			import * 
import numpy
import json
import sys
import re

# -------------------------------------------------------------------
# CGI SEARCH
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def cgi_search(request):
        search  = request.GET.get('term') or request.POST.get('term')
        list2   = []
	for q in Chapter.objects.filter(title__iregex=search)[0:3]:
        	list2.append({
        		"label": q.title,
 			"value": "/mind/chapter/%s/" % q.id,         
        		"category": 'Chapters',
        	})
	for q in Page.objects.filter(title__iregex=search)[0:5]:
        	list2.append({
        		"label": q.title,
 			"value": "/mind/page/read/%s/" % q.id,         
        		"category": 'Pages',
        	})
	return render_json(request,list2)

# -------------------------------------------------------------------
# DISPLAY ALL CHAPTERS
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def book(request):
	table = []
	qs = Chapter.objects.all().order_by('id')
	for i in range( 0, qs.count() ):
		d = { 'chapter':qs[i], 'number':i, }
		table.append(d)
	return render(request,"mind/templates/book.html",locals())

# -------------------------------------------------------------------
# PRINT 
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def worksheet(request): 
	table = Chapter.objects.all()
	return render(request,"mind/templates/print.html",locals())

# -------------------------------------------------------------------
# CHAPTER 
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def chapter(request,id):
	chapter = Chapter.objects.get(id=id)
	table = Page.objects.filter( chapter=chapter ) 
	return render(request,"mind/templates/chapter.html",locals())

# -------------------------------------------------------------------
# DELETE PAGE
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def page_delete(request,id):
	a = Page.objects.get( id=id ) 
	p = a.chapter.id
        a.delete()
        messages.add_message(request, messages.WARNING, "Page deleted!")
	return HttpResponseRedirect("/mind/chapter/%d/" %p)

# -------------------------------------------------------------------
# DELETE CHAPTER
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def delete(request,id):
	a = Chapter.objects.get( id=id ) 
	Page.objects.filter( chapter=a ).delete()	
        a.delete()
        messages.add_message(request, messages.WARNING, "Chapter deleted!")
	return HttpResponseRedirect("/mind/")

# -------------------------------------------------------------------
# EDIT CHAPTER
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def edit(request,id=None):

	# Load 
	# -------------------------------------------------------------------
	model = Chapter
	form = getform(model)
        req, non = getfields(model)

	# POST
	# -------------------------------------------------------------------
	if request.POST:

		# Update.-
		# -------------------------------------------------------------------
		if id:
        		elem = retrieve( model, id=id )
			form = form(request.POST,request.FILES,instance=elem)

		# Add.-
		# -------------------------------------------------------------------
		else:
			elem = model()	
			form = form(request.POST)

		# Non-required fields.-
		# -------------------------------------------------------------------
		for field in non: form.fields[field].required = False

		# Valid form.-
		# -------------------------------------------------------------------
		if not form.is_valid():
                	return render(request,"mind/templates/form.html",locals())
		else:

			# Set fields.-
			# -------------------------------------------------------------------
			for field in non + req: 
				setattr( elem, field, form.cleaned_data[field] ) 

			# Save.-
			# -------------------------------------------------------------------
			elem.save()
			messages.add_message(request, messages.SUCCESS, "Saved!")

			# Render.-
			# -------------------------------------------------------------------
			return HttpResponseRedirect("/mind/chapter/%d/" % elem.id)

	# GET
	# -------------------------------------------------------------------
	else:

		# Load Form.-
		# -------------------------------------------------------------------
		if id:
        		elem = retrieve( model, id=id )
			form = form(instance=elem)
		else:
			form = form()

		# Render.-
		# -------------------------------------------------------------------
		return render(request,"mind/templates/form.html",locals())

# -------------------------------------------------------------------
# EDIT PAGE
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def page(request,id=None):

	# Load 
	# -------------------------------------------------------------------
	model = Page
	form = getform(model)
        req, non = getfields(model)

	# POST
	# -------------------------------------------------------------------
	if request.POST:

		# Update.-
		# -------------------------------------------------------------------
		if id:
        		elem = retrieve( model, id=id )
			form = form(request.POST,request.FILES,instance=elem)

		# Add.-
		# -------------------------------------------------------------------
		else:
			elem = model()	
			form = form(request.POST)

		# Non-required fields.-
		# -------------------------------------------------------------------
		for field in non: form.fields[field].required = False

		# Valid form.-
		# -------------------------------------------------------------------
		if not form.is_valid():
			messages.add_message(request, messages.ERROR, "Form invalid!")
                	return render(request,"mind/templates/page.html",locals())
		else:

			# Set fields.-
			# -------------------------------------------------------------------
			for field in non + req: 
				setattr( elem, field, form.cleaned_data[field] ) 

			# Save.-
			# -------------------------------------------------------------------
			elem.save()
			messages.add_message(request, messages.SUCCESS, "Saved!")

			# Render.-
			# -------------------------------------------------------------------
			return HttpResponseRedirect("/mind/page/read/%d/" % elem.id)

	# GET
	# -------------------------------------------------------------------
	else:

		# Load Form.-
		# -------------------------------------------------------------------
		if id:
        		elem = retrieve( model, id=id )
			form = form(instance=elem)
		else:
			form = form()

		# Render.-
		# -------------------------------------------------------------------
		return render(request,"mind/templates/page.html",locals())

# -------------------------------------------------------------------
# READ PAGE
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def read(request,id):

	# Load 
	# -------------------------------------------------------------------
	page = Page.objects.get(id=id)

	# Render.-
	# -------------------------------------------------------------------
	return render(request,"mind/templates/read.html",locals())

# -------------------------------------------------------------------
# EDIT AVATAR
# -------------------------------------------------------------------
@login_required
@permission_required('admin.kaizen')
def avatar(request,id):

	# Load 
	# -------------------------------------------------------------------
	chapter = Chapter.objects.get(id=id)
	form = getform(ChapterImage)

	# POST
	# -------------------------------------------------------------------
	if request.POST:

		# Update.-
		# -------------------------------------------------------------------
        	elem = retrieve( ChapterImage, chapter=chapter )
		form = form(request.POST,request.FILES,instance=elem)

		# Set fields.-
		# -------------------------------------------------------------------
		elem.set_img(image=request.FILES.get('image'))	

		# Save.-
		# -------------------------------------------------------------------
		i = elem.img
		n = elem.img.name
		elem.save()
		messages.add_message(request, messages.SUCCESS, "Saved!")

		# Render.-
		# -------------------------------------------------------------------
		return HttpResponseRedirect("/mind/chapter/%d/" % chapter.id)

	# GET
	# -------------------------------------------------------------------
	else:

		# Load Form.-
		# -------------------------------------------------------------------
		if id:
        		elem = retrieve( ChapterImage, chapter=chapter )
			form = form(instance=elem)
		else:
			form = form()

		# Render.-
		# -------------------------------------------------------------------
		return render(request,"mind/templates/avatar.html",locals())
