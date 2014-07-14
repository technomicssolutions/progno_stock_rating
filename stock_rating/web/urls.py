
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from views import Login, Dashboard, Administration, Users, SaveUser, ResetPassword, FieldSettings, Fields, SaveField, FunctionSettings

urlpatterns = patterns('',
    url(r'login/$', Login.as_view(), name="login"),
    url(r'logout/$', Login.as_view(), name="logout"),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'))),
    url(r'dashboard/$', login_required(Dashboard.as_view()), name="dashboard"),
    url(r'administration/$', login_required(Administration.as_view()), name="administration"),
    url(r'field_settings/$', login_required(FieldSettings.as_view()), name="field_settings"),
    url(r'function_settings/$', login_required(FunctionSettings.as_view()), name="function_settings"),
    url(r'users/$', login_required(Users.as_view()), name="users"),
    url(r'fields/$', login_required(Fields.as_view()), name="fields"),
    url(r'save_user/$', login_required(SaveUser.as_view()), name="save_user"),
    url(r'save_field/$', login_required(SaveField.as_view()), name="save_field"),
    url(r'reset_password/$', login_required(ResetPassword.as_view()), name="reset_password"),
)



