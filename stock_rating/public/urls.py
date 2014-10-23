
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from views import (Login, Logout, Home, Signup, StarRating, StarRatingReport, AddToWatchlist)

LOGIN_URL = '/login/'

urlpatterns = patterns('',

    url(r'^$', Home.as_view(), name="home"),
    url(r'^login/$', Login.as_view(), name="public_login"),
    url(r'^logout/$', Logout.as_view(), name="public_logout"),
    url(r'^signup/$', Signup.as_view(), name="signup"),
    url(r'^star_rating/$', login_required(StarRating.as_view(), login_url="/login/"), name="star_rating"),
    url(r'^star_rating_report/$', login_required(StarRatingReport.as_view(), login_url="/login/"), name="star_rating_report"),
    url(r'^add_to_watch_list/$', login_required(AddToWatchlist.as_view(), login_url="/login/"), name="add_to_watch_list"),

)



