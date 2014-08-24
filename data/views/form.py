from __future__ import division
from django.contrib.auth.models         import User
from django.contrib.auth.decorators     import login_required, permission_required
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
# MODIFY AN EXISTING ELEMENT.-
# -------------------------------------------------------------------
@login_required
def mod(request,type,id):
	return render(request,"data/templates/form.html",locals())

# -------------------------------------------------------------------
# REMOVE AN EXISITING ELEMENT.-
# -------------------------------------------------------------------
@login_required
def rem(request,type,id):
	return render(request,"data/templates/form.html",locals())
