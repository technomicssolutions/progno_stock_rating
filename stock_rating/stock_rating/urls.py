
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
	url(r'', include('public.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^progno/', include('web.urls')),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
)
