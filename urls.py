from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib import auth 
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns('',
		url(r'^kain/', 		include("kain2.urls"),					),
		url(r'^mind/', 		include("mind.urls"),					),
		url(r'^goals/', 	include("goals2.urls"),					),
		url(r'^kaizen/', 	include("kaizen3.urls"),				),
		url(r'^sabbat/', 	include("sabbat5.urls"),				),
		url(r'^login/', 	include("login.urls"),					),
		url(r'^users/', 	include("login.urls"),					),
		url(r'^admin/', 	include(admin.site.urls),				),	
		url(r'^redirect/', 	'views.redirect',		name='redirect',	),
    		url(r'^.*', 		'views.home',			name='home',		),
)
