
from django.conf.urls import patterns, url


from views import (Login,Logout, Dashboard, Administration, Users, SaveUser, ResetPassword, \
    FieldSettings, FunctionSettings, GeneralFunctions, ContinuityFunctions, \
    ConsistencyFunctions, DeleteField, Model, IndustryDetails, DeleteModel, DeleteUser, \
    ModelDetails, DeleteParameter, DataUpload, AnalyticalHeads, DeleteHead, FieldMapping, \
    FileFields, OperatorsView, Companies, DeleteFunction, ModelStarRating, SaveModelStarRating, \
    RatingReport, DeleteRating, FieldsWithMapping, DeleteDataFile, RatingReportByStarCount, \
    RatingXML, progno_login_required, CompanyModelStarRating)

LOGIN_URL = '/progno/login/'

urlpatterns = patterns('',


    url(r'login/$', Login.as_view(), name="login"),
    url(r'logout/$', Logout.as_view(), name="logout"),

    url(r'dashboard/$', progno_login_required(Dashboard.as_view(), login_url= LOGIN_URL), name="dashboard"),
    url(r'administration/$', progno_login_required(Administration.as_view(), login_url= LOGIN_URL), name="administration"),
    url(r'field_settings/$', progno_login_required(FieldSettings.as_view(), login_url= LOGIN_URL), name="field_settings"),
    url(r'function_settings/$', progno_login_required(FunctionSettings.as_view(), login_url= LOGIN_URL), name="function_settings"),

    url(r'data_upload/$', progno_login_required(DataUpload.as_view(), login_url= LOGIN_URL), name="data_upload"),
    url(r'field_mapping/$', progno_login_required(FieldMapping.as_view(), login_url= LOGIN_URL), name="field_mapping"),
    url(r'file_fields/$', progno_login_required(FileFields.as_view(), login_url= LOGIN_URL), name="file_fields"),
    url(r'delete_data_file/(?P<file_id>\d+)/$', progno_login_required(DeleteDataFile.as_view(), login_url= LOGIN_URL), name="delete_data_file"),

    url(r'analytical_heads/$', progno_login_required(AnalyticalHeads.as_view(), login_url= LOGIN_URL), name="analytical_heads"),
    url(r'models/$', progno_login_required(Model.as_view(), login_url= LOGIN_URL), name="models"),
    url(r'users/$', progno_login_required(Users.as_view(), login_url= LOGIN_URL), name="users"),
    # url(r'category/$', progno_login_required(Category.as_view()), name="category"),   
    url(r'industry/$', progno_login_required(IndustryDetails.as_view(), login_url= LOGIN_URL), name="industry"),

    url(r'general_function/$', progno_login_required(GeneralFunctions.as_view(), login_url= LOGIN_URL), name="general_function"),
    url(r'continuity_function/$', progno_login_required(ContinuityFunctions.as_view(), login_url= LOGIN_URL), name="continuity_function"),
    url(r'consistency_function/$', progno_login_required(ConsistencyFunctions.as_view(), login_url= LOGIN_URL), name="consistency_function"),
    url(r'model_details/$', progno_login_required(ModelDetails.as_view(), login_url= LOGIN_URL), name="model_details"),

    url(r'delete_field/$', progno_login_required(DeleteField.as_view(), login_url= LOGIN_URL), name="delete_field"),
    url(r'delete_head/$', progno_login_required(DeleteHead.as_view(), login_url= LOGIN_URL), name="delete_head"),
    url(r'delete_model/$', progno_login_required(DeleteModel.as_view(), login_url= LOGIN_URL), name="delete_model"),
    url(r'delete_user/$', progno_login_required(DeleteUser.as_view(), login_url= LOGIN_URL), name="delete_user"),    
    url(r'delete_parameters/$', progno_login_required(DeleteParameter.as_view(), login_url= LOGIN_URL), name="delete_parameters"),
    url(r'delete_rating/$', progno_login_required(DeleteRating.as_view(), login_url= LOGIN_URL), name="delete_rating"),
    url(r'delete_function/(?P<function_id>\d+)/$', progno_login_required(DeleteFunction.as_view(), login_url= LOGIN_URL), name="delete_function"),

    url(r'save_user/$', progno_login_required(SaveUser.as_view(), login_url= LOGIN_URL), name="save_user"),
    url(r'reset_password/$', progno_login_required(ResetPassword.as_view(), login_url= LOGIN_URL), name="reset_password"),
    url(r'operators/$', progno_login_required(OperatorsView.as_view(), login_url= LOGIN_URL), name="operators"),

    url(r'companies/$', progno_login_required(Companies.as_view(), login_url= LOGIN_URL), name="companies"),
    url(r'model/(?P<model_id>\d+)/star_rating/$', progno_login_required(ModelStarRating.as_view(), login_url= LOGIN_URL), name="star_rating"),
    url(r'model/(?P<model_id>\d+)/save_star_rating/$', progno_login_required(SaveModelStarRating.as_view(), login_url= LOGIN_URL), name="save_star_rating"),
    url(r'rating_report_by_starcount/$', progno_login_required(RatingReportByStarCount.as_view(), login_url= LOGIN_URL), name="rating_report_by_starcount"),
    url(r'rating_report/$', progno_login_required(RatingReport.as_view(), login_url= LOGIN_URL), name="rating_report"),
    url(r'fields_with_mapping/$', progno_login_required(FieldsWithMapping.as_view(), login_url= LOGIN_URL), name="fields_with_mapping"),
    url(r'rating_xml/$', progno_login_required(RatingXML.as_view(), login_url= LOGIN_URL), name="rating_xml"), 
    url(r'company_model_starrating/$', progno_login_required(CompanyModelStarRating.as_view(), login_url= LOGIN_URL), name="company_model_starrating"),       
)



