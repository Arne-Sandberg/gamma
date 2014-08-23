from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import auth 
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
		url(r'^data/', 		include("data.urls"),					),
		url(r'^login/', 	include("login.urls"),					),
		url(r'^admin/', 	include(admin.site.urls),				),	
    		url(r'^.*', 		'views.home',			name='home',		),
)
