from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.forms import ModelForm
from django.conf import settings
from django.contrib import auth
from django.db.models import Q 
from datetime import datetime
from random import randrange
from django import forms
from libs.shared import *

# --------------------------------------------
# LOGIN 
# --------------------------------------------
def login(request):

	# Initialize variables
	username = None
	password = None

	# Get username and password from POST request.-
	if request.method == "POST":

		# Load parameters.-
		username = request.POST.get('usuario', None)
		password = request.POST.get('password', None)

		# Try to guess the username.-
		u = retrieve( User, username=username ) 

		if not u or not u.id:
			message = "El usuario no existe!"
			message = u

		# Validate that there there's user and password
		elif not username or not password:
			message = "Completar todos los datos!"

		# Validate username.-
		else:

			# Authenticate.-
			user = auth.authenticate(username=username,password=password)

			# Wrong credentials.-
			if user is None:
				message="Usuario inexistente!"

			# Account has been disabled.-
			elif not user.is_active:
				message="Usuario bloqueado!"

			# Login is ok!
			else:

				# Welcome user.-
				auth.login(request,user)
				messages.add_message(request, messages.SUCCESS, 'Bienvenido '+user.username+'!!')

				# Redirect to last page or home, instead.-
				if request.GET.get('next', False):
					return HttpResponseRedirect(request.GET.get('next'))
				else:
					return HttpResponseRedirect("/home/")

	# Go to login page.-
	return render(request,"login/templates/login.html", locals())

# --------------------------------------------
# LOGOUT
# --------------------------------------------
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login/")

