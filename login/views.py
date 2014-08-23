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
		username = request.POST.get('username', None)
		password = request.POST.get('password', None)

		# Try to guess the username.-
		u = retrieve( User, username=username ) 

		if not u or not u.id:
			message = "User does not exist"

		# Validate that there there's user and password
		elif not username or not password:
			message = "Complete all fields!"

		# Validate username.-
		else:

			# Authenticate.-
			user = auth.authenticate(username=username,password=password)

			# Wront credentials.-
			if user is None:
				message="Try again!"

			# Account has been disabled.-
			elif not user.is_active:
				message="User is blocked!"

			# Login is ok!
			else:

				# Welcome user.-
				auth.login(request,user)
				messages.add_message(request, messages.SUCCESS, 'Welcome '+user.username+'!!')

				# Redirect to last page or home, instead.-
				if request.GET.get('next', False):
					return HttpResponseRedirect(request.GET.get('next'))
				else:
					return HttpResponseRedirect("/home/")

	# Go to login page.-
	return render(request,"login/templates/login.html", locals())

# --------------------------------------------
# REGISTER
# --------------------------------------------
def register(request):
	
	# Initialize variables.-
	username = None
	mail	 = None

	# Get username and password from POST request.-
	if request.method == "POST":

		# Load parameters.-
		username = request.POST.get('username', None)
		mail	 = request.POST.get('mail', 	None)

		# Incomplete fields.-
		if not username or not mail:
			message = "Complete all fields!"

		# Validate username and password.-
		elif request.method == "POST":

			# Check Username.-
			if User.objects.filter(username=username): 	
					message = "Name already taken"

			else:

				# Create user.-
				u = User( username=username, email=mail )
				u.save()

				# Generate random password.-
				p = randrange(500000,1000000)
				u.set_password(p)
				u.save()

				# Add to Guest group.-
				group = Group.objects.get(name='Guest')
				u.groups.add(group)

				# Send mail with the confirmation.-
				s = "Phi! Password"
				m = " Dear %s, you can now login to phi! using the following password: %s " % ( username, p )
				f = "phi"	
				t = [ mail ]
				send_mail(s,m,f,t)	

				# Return to the register box.-
				message = "Success! Check your inbox"
			
	# Go to register page.-
	return render(request,"login/templates/register.html", locals())

# --------------------------------------------
# LOGOUT
# --------------------------------------------
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/login/")

# --------------------------------------------
# USERS
# --------------------------------------------
def users(request,name):
        user = User.objects.get(username=name)
        return render(request,"login/templates/users.html", locals())

