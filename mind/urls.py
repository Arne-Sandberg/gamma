from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

# -----------------------------------------------------
# Distpatch URLs.-
# -----------------------------------------------------
urlpatterns = patterns("mind.views",
		url(r'^cgi/search/$',		"cgi_search",		name='mind_cgi',   	),
		url(r'^page/read/(.*)/$',	"read",			name='mind_pread',   	),
		url(r'^page/edit/(.*)/$',	"page",			name='mind_pedit',   	),
		url(r'^page/add/$',		"page",			name='mind_padd',   	),
		url(r'^page/delete/(.*)/$',	"page_delete",		name='mind_pdel',   	),
		url(r'^avatar/(.*)/$',		"avatar",		name='mind_avatar',   	),
		url(r'^add/$',			"edit",			name='mind_add',   	),
		url(r'^edit/(.*)/$',		"edit",			name='mind_edit',   	),
		url(r'^chapter/(.*)/$',		"chapter",		name='mind_chapter',   	),
		url(r'^delete/(.*)/$',		"delete",		name='mind_del',   	),
		url(r'^print/$',		"worksheet",		name='mind_print',	),
		url(r'^book/$',			"book",			name='mind_book',	),
		url(r'^.*$',			"book",			name='mind_home', 	),
)
