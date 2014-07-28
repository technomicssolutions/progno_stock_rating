
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from views import Login,Logout, Dashboard, Administration, Users, SaveUser, ResetPassword, \
    FieldSettings, Fields, SaveField, FunctionSettings, SaveFunction, Category, Analyt_Heads, \
    Functions, General, Continuity, Consistency, DeleteField, Model, IndustryDetails, SaveModel, \
    ModelDetails, DeleteModel, DeleteUser, ModelView, SaveParameters

urlpatterns = patterns('',
    url(r'login/$', Login.as_view(), name="login"),
    url(r'logout/$', Logout.as_view(), name="logout"),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'))),
    url(r'dashboard/$', login_required(Dashboard.as_view()), name="dashboard"),
    url(r'administration/$', login_required(Administration.as_view()), name="administration"),
    url(r'field_settings/$', login_required(FieldSettings.as_view()), name="field_settings"),
    url(r'function_settings/$', login_required(FunctionSettings.as_view()), name="function_settings"),
    url(r'models/$', login_required(Model.as_view()), name="models"),
    url(r'users/$', login_required(Users.as_view()), name="users"),
    url(r'fields/$', login_required(Fields.as_view()), name="fields"),
    url(r'category/$', login_required(Category.as_view()), name="category"),
    url(r'models_list/$', login_required(ModelDetails.as_view()), name="models_list"),
    url(r'industry/$', login_required(IndustryDetails.as_view()), name="industry"),
    url(r'anly_head/$', login_required(Analyt_Heads.as_view()), name="anly_head"),
    url(r'functions/$', login_required(Functions.as_view()), name="functions"),
    url(r'get_general/$', login_required(General.as_view()), name="get_general"),
    url(r'get_continuity/$', login_required(Continuity.as_view()), name="get_continuity"),
    url(r'get_consistency/$', login_required(Consistency.as_view()), name="get_consistency"),
    url(r'get_model_details/$', login_required(ModelView.as_view()), name="get_model_details"),
    url(r'delete_field/$', login_required(DeleteField.as_view()), name="delete_field"),
    url(r'delete_model/$', login_required(DeleteModel.as_view()), name="delete_model"),
    url(r'delete_user/$', login_required(DeleteUser.as_view()), name="delete_user"),
    url(r'save_user/$', login_required(SaveUser.as_view()), name="save_user"),
    url(r'save_field/$', login_required(SaveField.as_view()), name="save_field"),
    url(r'save_model/$', login_required(SaveModel.as_view()), name="save_model"),
    url(r'save_function/$', login_required(SaveFunction.as_view()), name="save_function"),
    url(r'save_parameters/$', login_required(SaveParameters.as_view()), name="save_parameters"),
    url(r'reset_password/$', login_required(ResetPassword.as_view()), name="reset_password"),
)



