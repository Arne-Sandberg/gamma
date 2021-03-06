from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import auth 
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
		url(r'^folder/', 	include("folder.urls"),					),
		url(r'^gallery/',	include("gallery.urls"),				),
		url(r'^login/', 	include("login.urls"),					),
		url(r'^search/', 	include("search.urls"),					),
		url(r'^admin/', 	include(admin.site.urls),				),	
    		url(r'^.*', 		'views.home',			name='home',		),
)
