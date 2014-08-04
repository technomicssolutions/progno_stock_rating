
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from views import Login,Logout, Dashboard, Administration, Users, SaveUser, ResetPassword, \
    FieldSettings, FunctionSettings, Category, General, Continuity, Consistency, \
    DeleteField, Model, IndustryDetails, DeleteModel, DeleteUser, ModelDetails, \
    DeleteParameter, DataUpload, AnalyticalHeads, DeleteHead, FieldMapping, FileFields

urlpatterns = patterns('',

    url(r'^$', RedirectView.as_view(url=reverse_lazy('dashboard'))),

    url(r'login/$', Login.as_view(), name="login"),
    url(r'logout/$', Logout.as_view(), name="logout"),

    url(r'dashboard/$', login_required(Dashboard.as_view()), name="dashboard"),
    url(r'administration/$', login_required(Administration.as_view()), name="administration"),
    url(r'field_settings/$', login_required(FieldSettings.as_view()), name="field_settings"),
    url(r'function_settings/$', login_required(FunctionSettings.as_view()), name="function_settings"),

    url(r'data_upload/$', login_required(DataUpload.as_view()), name="data_upload"),
    url(r'field_mapping/$', login_required(FieldMapping.as_view()), name="field_mapping"),
    url(r'file_fields/$', login_required(FileFields.as_view()), name="file_fields"),

    url(r'analytical_heads/$', login_required(AnalyticalHeads.as_view()), name="analytical_heads"),
    url(r'models/$', login_required(Model.as_view()), name="models"),
    url(r'users/$', login_required(Users.as_view()), name="users"),
    url(r'category/$', login_required(Category.as_view()), name="category"),   
    url(r'industry/$', login_required(IndustryDetails.as_view()), name="industry"),

    url(r'get_general/$', login_required(General.as_view()), name="get_general"),
    url(r'get_continuity/$', login_required(Continuity.as_view()), name="get_continuity"),
    url(r'get_consistency/$', login_required(Consistency.as_view()), name="get_consistency"),
    url(r'model_details/$', login_required(ModelDetails.as_view()), name="model_details"),

    url(r'delete_field/$', login_required(DeleteField.as_view()), name="delete_field"),
    url(r'delete_head/$', login_required(DeleteHead.as_view()), name="delete_head"),
    url(r'delete_model/$', login_required(DeleteModel.as_view()), name="delete_model"),
    url(r'delete_user/$', login_required(DeleteUser.as_view()), name="delete_user"),    
    url(r'delete_parameters/$', login_required(DeleteParameter.as_view()), name="delete_parameters"),

    url(r'save_user/$', login_required(SaveUser.as_view()), name="save_user"),
    url(r'reset_password/$', login_required(ResetPassword.as_view()), name="reset_password"),
)



