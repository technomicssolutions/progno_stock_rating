from django.contrib import admin
from web.models import *


def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=stocks.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"Name"),
        smart_str(u"ISIN"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.company_name),
            smart_str(obj.isin_code),
        ])
    return response
export_csv.short_description = u"Export CSV"

def export_xls(modeladmin, request, queryset):
    import xlwt
    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=stocks.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Stocka")
    
    row_num = 0
    
    columns = [
        (u"Name", 2000),
        (u"ISIN", 6000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for obj in queryset:
        row_num += 1
        row = [
            obj.company_name,
            obj.isin_code,
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
    
export_xls.short_description = u"Export XLS"

# def export_xlsx(modeladmin, request, queryset):
#     import openpyxl
#     from openpyxl.cell import get_column_letter
#     response = HttpResponse(mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename=stocks.xlsx'
#     wb = openpyxl.Workbook()
#     ws = wb.get_active_sheet()
#     ws.title = "Stocks"

#     row_num = 0

#     columns = [
#         (u"Name", 15),
#         (u"ISIN", 70),
#     ]

#     for col_num in xrange(len(columns)):
#         c = ws.cell(row=row_num + 1, column=col_num + 1)
#         c.value = columns[col_num][0]
#         c.style.font.bold = True
#         # set column width
#         ws.column_dimensions[get_column_letter(col_num+1)].width = columns[col_num][1]

#     for obj in queryset:
#         row_num += 1
#         row = [
#             obj.company_name,
#             obj.isin_code,
#         ]
#         for col_num in xrange(len(row)):
#             c = ws.cell(row=row_num + 1, column=col_num + 1)
#             c.value = row[col_num]
#             c.style.alignment.wrap_text = True

#     wb.save(response)
#     return response
# export_xlsx.short_description = u"Export XLSX"

class UserPermissionAdmin(admin.ModelAdmin):
    search_fields = ['username']

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['industry__industry_name', 'company_name']
    list_filter = ('is_all_data_available',)
    actions = [export_csv, export_xls]
        


class IndustryAdmin(admin.ModelAdmin):
    search_fields = ['industry_name']

class CompanyFunctionScoreAdmin(admin.ModelAdmin):
    search_fields = ['company__company_name', 'function__function_name']

class CompanyModelScoreAdmin(admin.ModelAdmin):
    search_fields = ['company__company_name', 'analysis_model__name']

class CompanyStockDataAdmin(admin.ModelAdmin):
    search_fields = ['company__company_name']

class CompanyModelFunctionPointAdmin(admin.ModelAdmin):
    search_fields = ['company__company_name', 'parameter_limit__function__function_name', 'parameter_limit__analysis_model__name']

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
admin.site.register(AnalysisModel)
admin.site.register(ParameterLimit)
admin.site.register(StarRating)
admin.site.register(CompanyFunctionScore, CompanyFunctionScoreAdmin)
admin.site.register(CompanyModelScore, CompanyModelScoreAdmin)
admin.site.register(CompanyFile)
admin.site.register(CompanyStockData, CompanyStockDataAdmin)
admin.site.register(CompanyModelFunctionPoint, CompanyModelFunctionPointAdmin)
admin.site.register(NSEBSEPrice, NSEBSEPriceAdmin)



