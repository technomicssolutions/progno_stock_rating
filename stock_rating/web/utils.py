
import xlrd
from django.conf import settings
from collections import OrderedDict
from models import Company, Industry, CompanyStockData

def process_data_file(data_file):
    sheets = []
    workbook = xlrd.open_workbook(settings.MEDIA_ROOT+'/'+data_file.uploaded_file.name)
    worksheets = workbook.sheet_names()
    data_file.number_of_sheets = len(worksheets)
    data_file.save()
    for worksheet_name in worksheets:
        sheet = OrderedDict({
            'name_of_sheet': '',
            'rows': ''
        })
        sheet['name_of_sheet'] = worksheet_name
        rows = []
        worksheet = workbook.sheet_by_name(worksheet_name)
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        curr_row = -1            
        curr_cell = -1
        while curr_row < num_rows:
            curr_row += 1                
            curr_cell = -1
            row = []
            if curr_row != 0:
                for x in rows[0]:
                    row.append(x)
            while curr_cell < num_cells:
                curr_cell += 1
                # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                #cell_type = worksheet.cell_type(curr_row, curr_cell)
                cell_value = worksheet.cell_value(curr_row, curr_cell)
                if curr_row != 0 :
                    field_name = worksheet.cell_value(0, curr_cell)
                    index = rows[0].index(field_name)
                    row[index] = cell_value
                else:
                    row.append(cell_value)
            if curr_row == 0:
                row = list(OrderedDict.fromkeys(row))
                rows.append(row)
            else:
                rows.append(row)
        sheet['rows'] = rows
        sheets.append(sheet)
    data_file.save()
    create_stock_data(data_file)    
    return sheets


def process_company_file(data_file, request):
    workbook = xlrd.open_workbook(settings.MEDIA_ROOT+'/'+data_file.uploaded_file.name)
    worksheets = workbook.sheet_names()
    data_file.number_of_sheets = len(worksheets)
    data_file.save()
    for worksheet_name in worksheets:
        worksheet = workbook.sheet_by_name(worksheet_name)
        num_rows = worksheet.nrows - 1
        curr_row = 0            
        while curr_row < num_rows:
            curr_row += 1                
            company_name = worksheet.cell_value(curr_row, 0)
            industry = worksheet.cell_value(curr_row, 1)
            isin = worksheet.cell_value(curr_row, 2)
            industry, created = Industry.objects.get_or_create(industry_name=industry)
            industry.created_by = data_file.uploaded_by
            industry.save()
            company, created = Company.objects.get_or_create(isin_code=isin)
            company.industry = industry
            company.company_name = company_name
            company.created_by = data_file.uploaded_by
            company.save()
    data_file.processing_completed = True
    data_file.save()
    # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
    #cell_type = worksheet.cell_type(curr_row, curr_cell)

def create_stock_data(data_file):

    for sheet in data_file.sheets:
        company_stock = None
        labels = sheet['rows'][0]
        for row in sheet['rows']:
            for i in range(len(row)):
                if i == 0:
                    try:
                        company = Company.objects.get(isin_code=row[i])
                        company_stock, created = CompanyStockData.objects.get_or_create(company=company)
                    except:
                        continue
                else:
                    if company_stock:
                        if company_stock.stock_data == None:
                            company_stock.stock_data = {}
                        company_stock.stock_data[labels[i]] = row[i]
                        company_stock.created_by = data_file.uploaded_by
                        company_stock.save()
    data_file.processing_completed = True
    data_file.save()
