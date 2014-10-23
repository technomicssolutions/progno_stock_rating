
import xlrd
import simplejson

from django.conf import settings
from collections import OrderedDict
from models import Company, Industry, CompanyStockData, CompanyFunctionScore, \
 FieldMap, DataFile, CompanyModelScore, CompanyModelFunctionPoint

from public.models import WatchList, CompareList, PublicUser

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
                cell_value = worksheet.cell_value(curr_row, curr_cell)
                if curr_row != 0 :
                    field_name = worksheet.cell_value(0, curr_cell)
                    index = rows[0].index(field_name)
                    if row[index] == field_name:
                        row[index] = cell_value
                    elif cell_value != '':
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
    data_file.sheets = sheets
    data_file.save()
    create_stock_data(data_file)    
    return sheets

def process_company_file(data_file):
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

def create_stock_data(data_file):
    for sheet in data_file.sheets:
        company_stock = None
        if len(sheet['rows']) > 0:
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
                            if row[i] == '':
                                company.is_all_data_available = False
                                company.save()
    data_file.processing_completed = True
    data_file.save()

def calculate_general_function_score(function, company):
    stock = CompanyStockData.objects.get(company=company)
    stock = stock.stock_data
    function_operands = function.formula.operands.all()
    formula = function.formula.formula_string    
    function_value = ''
    for operand in function_operands:
        mapping = FieldMap.objects.get(data_field = operand)
        key_name = mapping.file_field
        if stock[key_name] != '':
            vars()[operand.name] = float(stock[key_name])
        else:
            vars()[operand.name] = stock[key_name]
    try:
        function_value = eval(formula)
        function_score, created = CompanyFunctionScore.objects.get_or_create(company=company, function=function)
        function_score.score = function_value 
        function_score.save()        
        function_score.save()
    except Exception as e:       
        pass
    return function_value

def calculate_consistency_function_score(function, company):
    stock = CompanyStockData.objects.get(company=company)
    function_operands = function.consistencyfunction.fields.all()
    num_of_periods = function.consistencyfunction.number_of_fields + function.consistencyfunction.number_of_functions
    operands_sum = 0
    data_values = []
    for operand in function_operands:       
        mapping = FieldMap.objects.get(data_field = operand)
        key_name = mapping.file_field
        operands_sum = operands_sum + stock.stock_data[key_name]
        data_values.append(stock.stock_data[key_name])
    for fun in function.consistencyfunction.functions.all():        
        try:
            value = CompanyFunctionScore.objects.get(function=fun, company=company)     
            value = value.score       
        except:
            value = calculate_general_function_score(fun, company)        
        operands_sum = operands_sum + value
        data_values.append(value)   
    avg = float(operands_sum)/float(num_of_periods)
    benchmark = (avg-1.5)
    performance_count = 0
    for value in data_values:
        if value >= benchmark:
            performance_count = performance_count + 1
    performance_percentage = float(performance_count)/float(num_of_periods)*100
    function_score, created = CompanyFunctionScore.objects.get_or_create(company=company, function=function)
    function_score.score = performance_percentage     
    function_score.save()

def calculate_continuity_function_score(function, company):
    stock = CompanyStockData.objects.get(company=company)
    num_of_periods = function.continuityfunction.number_of_fields + function.continuityfunction.number_of_functions
    performance_count = 0
    for fun in function.continuityfunction.functions.all():       
        try:
            value = CompanyFunctionScore.objects.get(function=fun, company=company) 
            value = value.score           
        except:
            value = calculate_general_function_score(fun, company)
        if value > 0:
            performance_count = performance_count + 1
    for operand in function.continuityfunction.fields.all():
        mapping = FieldMap.objects.get(data_field = operand)
        key_name = mapping.file_field
        if float(stock.stock_data[key_name]) > 0:
            performance_count = performance_count + 1 
    
    performance_percentage = float(performance_count)/float(num_of_periods)*100
    function_score, created = CompanyFunctionScore.objects.get_or_create(company=company, function=function)
    function_score.score = performance_percentage 
    function_score.save()


def get_file_fields():
    data_files = DataFile.objects.all()
    file_fields = []
    for d_file in data_files:
        for sheet in d_file.sheets:
            if len(sheet['rows']) > 0:
                file_fields = list(set(file_fields + sheet['rows'][0]))
    return file_fields

def get_rating_details_by_star_count(request, star_count):
    ratings = []
    isin_list = []
    model_scores = CompanyModelScore.objects.filter(star_rating=star_count)
    for model_score in model_scores:
        model = model_score.analysis_model
        company = model_score.company
        isin_list.append(company.isin_code)
        parameters = model.parameterlimit_set.all()
        comments = []
        for parameter in parameters:
            function = parameter.function
            fun_score = CompanyModelFunctionPoint.objects.filter(company=company, function=function, model=model)
            if fun_score.count() > 0:
                comments.append(fun_score[0].comment)
        ratings.append({
            'company_name': company.company_name + ' - ' + company.isin_code,
            'isin_code': company.isin_code,
            'industry': company.industry.industry_name,
            'star_rating': "*" * int(model_score.star_rating) if model_score.star_rating else '',
            'score': model_score.points,
            'brief_comment': model_score.comment,
            'detailed_comment': comments,
            'rating_changed_date': model_score.updated_date.strftime('%d/%m/%Y'),
        })
    watchlist_companies = 0
    comparelist_companies = 0
    try:
        public_user = PublicUser.objects.get(user=request.user)
        watch_list = public_user.watchlist_set.all()
        if watch_list.count() > 0:
            watchlist_companies = watch_list[0].companies.all().count()
        compare_list = public_user.comparelist_set.all()
        if compare_list.count() > 0:
            comparelist_companies = compare_list[0].companies.all().count()
    except:
        pass
    response = simplejson.dumps({
        'star_ratings': ratings,
        'isin_list': isin_list,
        'watch_list_count': watchlist_companies,
        'compare_list_count': comparelist_companies,
    })
    return response

def get_rating_report(request, search_keys):
    ratings = []
    isin_list = []
    for key in search_keys:
        company = Company.objects.get(isin_code=key)
        isin_list.append(company.isin_code)
        model_score = CompanyModelScore.objects.filter(company=company)
        if model_score.count() > 0:
            model_score = model_score[0]
            rating = {
                'company_name': company.company_name + ' - ' + company.isin_code,
                'industry': company.industry.industry_name,
                'star_rating': "*" * int(model_score.star_rating) if model_score.star_rating else '',
                'score': model_score.points,
                'brief_comment': model_score.comment,
            }
            model = model_score.analysis_model
            parameters = model.parameterlimit_set.all()
            comments = []
            for parameter in parameters:
                function = parameter.function
                fun_score = CompanyModelFunctionPoint.objects.filter(company=company, function=function, model=model)
                if fun_score.count() > 0:
                    comments.append(fun_score[0].comment)
            analytical_heads = []
            for analytical_head in model.analytical_heads.all():
                functions_details = []

                for function in analytical_head.function_set.all():
                    comments = []
                    fun_score = CompanyModelFunctionPoint.objects.filter(company=company, function=function, model=model)
                    if fun_score.count() > 0:
                        comments.append(fun_score[0].comment)
                    function_score = CompanyFunctionScore.objects.get(function=function, company=company)
                    functions_details.append({
                        'function_name': function.function_name + str(' - ') + str(function_score.score),
                        'score': function_score.score,
                        'description': function.description,
                        'comments': comments[0] if len(comments) > 0 else 'None'
                    })
                analytical_heads.append({
                    'analytical_head_name': analytical_head.title,
                    'functions': functions_details,
                })
            rating['analytical_heads'] = analytical_heads
            rating['detailed_comment'] = comments
        else:
            rating = {
                'company_name': company.company_name + ' - ' + company.isin_code,
                'star_rating': 'Data not available' if not company.is_all_data_available else 'No Rating available'
            }
        ratings.append(rating)
    public_user = PublicUser.objects.get(user=request.user)
    watch_list = public_user.watchlist_set.all()
    watchlist_companies = 0
    if watch_list.count() > 0:
        watchlist_companies = watch_list[0].companies.all().count()
    compare_list = public_user.comparelist_set.all()
    comparelist_companies = 0
    if compare_list.count() > 0:
        comparelist_companies = compare_list[0].companies.all().count()
    response = simplejson.dumps({
        'star_ratings': ratings,
        'isin_list': isin_list,
        'watch_list_count': watchlist_companies,
        'compare_list_count': comparelist_companies,
    })
    return response