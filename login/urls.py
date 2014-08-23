from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

# -----------------------------------------------------
# Distpatch URLs.-
# -----------------------------------------------------
urlpatterns = patterns("login.views",
		url(r'^register/$',	"register",	name='register',	),
		url(r'^logout/$',	"logout",	name='logout'		),
		url(r'^login/$',	"login",	name='login'		),
		url(r'^(.*)/$',		"users",	name='users'		),
		url(r'^.*$',		"login",	name='home_login',	),
)
