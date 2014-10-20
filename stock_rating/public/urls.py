
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from views import (Login, Logout, Home)

LOGIN_URL = '/login/'

urlpatterns = patterns('',

    url(r'^$', Home.as_view(), name="home"),
    url(r'^login/$', Login.as_view(), name="login"),
    url(r'^logout/$', Logout.as_view(), name="logout"),

)



