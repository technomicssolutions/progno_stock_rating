from django.contrib import admin
from web.models import *

import xml.etree.cElementTree as ET

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
        (u"Industry", 2000),
        (u"Score", 2000),
        (u"Starcount", 1000),
        (u"Brief Comment", 1000),
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
        model_score = CompanyModelScore.objects.filter(company=obj)
        if model_score.count() > 0:
            score = model_score[0].points
            stars = model_score[0].star_rating.star_count
            brief_comment = model_score[0].star_rating.comment
        else:
            score = ''
            stars = ''
            brief_comment = ''
        row_num += 1
        row = [
            obj.company_name,
            obj.isin_code,
            obj.industry.industry_name,
            score,
            stars,
            brief_comment
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
    
export_xls.short_description = u"Export XLS"

def export_xml(modeladmin, request, queryset):
    response = HttpResponse(mimetype='application/xml')
    response['Content-Disposition'] = 'attachment; filename=stocks.xml'
    root = ET.Element("COMPANIES")
    for obj in queryset:
        model_score = CompanyModelScore.objects.filter(company=obj)
        if model_score.count() > 0:
            score = str(model_score[0].points)
            stars = str(model_score[0].star_rating.star_count)
            brief_comment = str(model_score[0].star_rating.comment)
        else:
            score = ''
            stars = ''
            brief_comment = ''
        doc = ET.SubElement(root, "Company")

        field1 = ET.SubElement(doc, "Name")
        field1.text = obj.company_name

        field2 = ET.SubElement(doc, "ISIN")
        field2.text = obj.isin_code

        field3 = ET.SubElement(doc, "Score")
        field3.text = score

        field4 = ET.SubElement(doc, "Stars")
        field4.text = stars

        field5 = ET.SubElement(doc, "BriefComment")
        field5.text = brief_comment

    tree = ET.ElementTree(root)
    tree.write(response)
    return response

export_xml.short_description = u"Export XML"

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
    search_fields = ['industry__industry_name', 'company_name', 'isin_code']
    list_filter = ('is_all_data_available',)
    actions = [export_csv, export_xls, export_xml]
        
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

class BSEPriceAdmin(admin.ModelAdmin):
    search_fields = ['company__company_name']

class NSEPriceAdmin(admin.ModelAdmin):
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
admin.site.register(NSEPrice, NSEPriceAdmin)
admin.site.register(BSEPrice, BSEPriceAdmin)



