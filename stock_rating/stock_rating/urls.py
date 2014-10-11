
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'))),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^progno/', include('web.urls')),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),

)
