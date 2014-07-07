
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from views import Login, Dashboard

urlpatterns = patterns('',
    url(r'login/$', Login.as_view(), name="login"),
    url(r'logout/$', Login.as_view(), name="logout"),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'))),
    url(r'dashboard/$', login_required(Dashboard.as_view()), name="dashboard"),
)



