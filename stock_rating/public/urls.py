
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from views import (Login, Logout, Home, Signup)

LOGIN_URL = '/login/'

urlpatterns = patterns('',

    url(r'^$', Home.as_view(), name="home"),
    url(r'^login/$', Login.as_view(), name="public_login"),
    url(r'^logout/$', Logout.as_view(), name="public_logout"),
    url(r'^signup/$', Signup.as_view(), name="signup"),

)



