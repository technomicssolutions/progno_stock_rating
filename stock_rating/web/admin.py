from django.contrib import admin
from web.models import *

class UserPermissionAdmin(admin.ModelAdmin):
	search_fields = ['username']

class CompanyAdmin(admin.ModelAdmin):
	search_fields = ['industry__industry_name', 'company_name']

class IndustryAdmin(admin.ModelAdmin):
	search_fields = ['industry_name']

class CompanyFunctionScoreAdmin(admin.ModelAdmin):
	search_fields = ['company__company_name', 'function__function_name']

class CompanyModelScoreAdmin(admin.ModelAdmin):
	search_fields = ['company__company_name', 'analysis_model__name']

class CompanyStockDataAdmin(admin.ModelAdmin):
	search_fields = ['company__company_name']

class CompanyModelFunctionPointAdmin(admin.ModelAdmin):
	search_fields = ['company__company_name', 'function__function_name', 'model__name']

class NSEBSEPriceAdmin(admin.ModelAdmin):
	search_fields = ['company__company_name']

admin.site.register(UserPermission, UserPermissionAdmin)
admin.site.register(AnalyticalHead)
admin.site.register(DataField)
admin.site.register(DataFile)
admin.site.register(FieldMap)
admin.site.register(Operator)
admin.site.register(Formula)
admin.site.register(Function)
admin.site.register(HardcodedFormula)
admin.site.register(ContinuityFunction)
admin.site.register(ConsistencyFunction)
admin.site.register(Industry, IndustryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(ScoreRating)
admin.site.register(AnalysisModel)
admin.site.register(ParameterLimit)
admin.site.register(StarRating)
admin.site.register(CompanyFunctionScore, CompanyFunctionScoreAdmin)
admin.site.register(CompanyModelScore, CompanyModelScoreAdmin)
admin.site.register(CompanyFile)
admin.site.register(CompanyStockData, CompanyStockDataAdmin)
admin.site.register(CompanyModelFunctionPoint, CompanyModelFunctionPointAdmin)
admin.site.register(NSEBSEPrice, NSEBSEPriceAdmin)



