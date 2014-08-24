from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib import messages
from django.contrib import auth
from libs.shared import *

# --------------------------------------------
# PRINT HOME
# --------------------------------------------
def home(request):
        return render(request,"templates/home.html", locals())

