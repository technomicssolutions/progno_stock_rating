
from django.conf.urls import patterns, url
from django.views.decorators.vary import vary_on_headers


from views import (Login, Logout, Home, Signup, StarRating, StarRatingReport, \
	VerifyRecaptcha, AddToWatchlist, AddToComparelist, ViewWatchList, public_login_required,\
     ViewCompareList, SearchResult, SearchCompany, DeleteFromCompareList, ChangeCompareList, \
     HelpView, ActivateAccount, TermsOfUse, Disclaimer, PrivacyPolicy, FBLoginRedirect, ForgotPassword,\
     ResetPassword)

LOGIN_URL = '/login/'

urlpatterns = patterns('',

    url(r'^$', Home.as_view(), name="home"),
    url(r'^fb_login_redirect/$', FBLoginRedirect.as_view(), name="fb_login_redirect"),
    url(r'^login/$', Login.as_view(), name="public_login"),
    url(r'^logout/$', Logout.as_view(), name="public_logout"),
    url(r'^signup/$', Signup.as_view(), name="signup"),
    url(r'^star_rating/$', public_login_required(vary_on_headers('X_REQUESTED_WITH')(StarRating.as_view()), login_url="/login/"), name="star_rating"),
    url(r'^star_rating_report/$', public_login_required(vary_on_headers('X_REQUESTED_WITH')(StarRatingReport.as_view()), login_url="/login/"), name="star_rating_report"),
    url(r'^verify_recaptcha/$', VerifyRecaptcha.as_view(), name="verifiy_recaptcha"),
    url(r'^add_to_watch_list/$', public_login_required(AddToWatchlist.as_view(), login_url="/login/"), name="add_to_watch_list"),
    url(r'^add_to_compare_list/$', public_login_required(AddToComparelist.as_view(), login_url="/login/"), name="add_to_compare_list"),
    url(r'^add_to_compare_list/$', public_login_required(AddToComparelist.as_view(), login_url="/login/"), name="add_to_compare_list"),
    url(r'^compare_list/$', public_login_required(vary_on_headers('X_REQUESTED_WITH')(ViewCompareList.as_view()), login_url="/login/"), name="compare_list"),
    url(r'^change_compare_list/$', public_login_required(ChangeCompareList.as_view(), login_url="/login/"), name="change_compare_list"),
    url(r'^watch_list/$', public_login_required(vary_on_headers('X_REQUESTED_WITH')(ViewWatchList.as_view()), login_url="/login/"), name="watch_list"),
    url(r'^search_result/$', vary_on_headers('X_REQUESTED_WITH')(SearchResult.as_view()), name="search_result"),
    url(r'^search_company/$', vary_on_headers('X_REQUESTED_WITH')(SearchCompany.as_view()), name="search_company"),
    url(r'^delete_from_compare_list/$', public_login_required(DeleteFromCompareList.as_view(), login_url="/login/"), name="delete_from_compare_list"),
    url(r'^help/$', public_login_required(HelpView.as_view(), login_url="/login/"), name="help"),
    url(r'^activate/$', ActivateAccount.as_view(), name="activate_account"),
    url(r'^terms_of_use/$', TermsOfUse.as_view(), name="terms_of_use"),
    url(r'^disclaimer/$', Disclaimer.as_view(), name="disclaimer"),
    url(r'^privacy_policy/$', PrivacyPolicy.as_view(), name="privacy_policy"),
    url(r'^forgot_password/$', ForgotPassword.as_view(), name="forgot_password"),
    url(r'^reset_password/$', ResetPassword.as_view(), name="reset_password"),
)



