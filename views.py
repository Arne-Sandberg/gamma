from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
from libs.shared import *
from folder.models import * 
import subprocess
import commands
import os

# --------------------------------------------
# PRINT HOME
# --------------------------------------------
def home(request):

	# Get newest files.-
	table = GFile.objects.filter(folder__read=True,type__in=['IMG','']).order_by('date')[:10]

	# Calculate FileSystem df.-
	cmd = "df -Ph "+ settings.MEDIA_ROOT+" | tail -1 |  awk '{print $5}' "
	df = commands.getstatusoutput(cmd)[1]
	MEDIA_ROOT = settings.MEDIA_ROOT

	# Return.-
        return render(request,"templates/home.html", locals())

