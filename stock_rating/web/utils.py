
import xlrd
import simplejson

from django.conf import settings
from collections import OrderedDict
from models import Company, Industry, CompanyStockData, CompanyFunctionScore, ParameterLimit, \
 FieldMap, DataFile, CompanyModelScore, CompanyModelFunctionPoint, NSEBSEPrice

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

def get_rating_details_by_star_count(request, star_count, order_by, start, end):
    ratings = []
    isin_list = []
    if start == '':
        start = 0
    if end == '':
        end = 10
    model_scores = CompanyModelScore.objects.filter(star_rating__star_count=star_count).order_by('score')
    total_count = model_scores.count()
    try:
        model_scores = model_scores[int(start):int(end)]
    except:
        model_scores = model_scores[int(start):]
    if order_by == 'company_name':
        model_scores = CompanyModelScore.objects.filter(star_rating__star_count=star_count).order_by('company__company_name')[int(start):int(end)]
    public_user = PublicUser.objects.filter(user=request.user)
    for model_score in model_scores:
        model = model_score.analysis_model
        company = model_score.company
        if company.is_all_data_available:
            company_in_watch_list = False
            company_in_compare_list = False
            if model_score.star_rating_change and model_score.star_rating_change > 0:
                change_in_star_rating = ' up by '+str("*" * int(model_score.star_rating_change))
            elif model_score.star_rating_change and model_score.star_rating_change < 0:
                change_in_star_rating = ' down by '+str("*" * abs(model_score.star_rating_change))
            else:
                change_in_star_rating = ' '
            if public_user.count() > 0:
                try:
                    watch_list = WatchList.objects.get(company=company, user=public_user[0])
                    company_in_watch_list = True
                except:
                    company_in_watch_list = False
                try:
                    compare_list = CompareList.objects.get(company=company, user=public_user[0])
                    company_in_compare_list = True
                except:
                    company_in_compare_list = False
            isin_list.append(company.isin_code)
            parameters = model.parameterlimit_set.all()
            comments = []
            for parameter in parameters:
                function = parameter.function
                fun_score = CompanyModelFunctionPoint.objects.filter(company=company, parameter_limit=parameter)
                if fun_score.count() > 0:
                    fun_score = fun_score[0]
                    if fun_score.points == parameter.strong_points:
                        comments.append(parameter.strong_comment)
                    elif fun_score.points == parameter.weak_points:
                        comments.append(parameter.weak_comment)
                    elif fun_score.points == parameter.neutral_points:
                        comments.append(parameter.neutral_comment)
            pricing = {}
            try:
                price = NSEBSEPrice.objects.get(company=company, latest=True)
                pricing = {
                    'nse_price': price.NSE_price,
                    'bse_price': price.BSE_price,
                    'date': price.date.strftime('%d %B %Y')
                }
            except Exception as ex:
                print str(ex)
                pass
            ratings.append({
                'company_name': company.company_name + ' - ' + company.isin_code,
                'isin_code': company.isin_code,
                'industry': company.industry.industry_name,
                'star_rating': "*" * int(model_score.star_rating.star_count) if model_score.star_rating else '',
                'score': str(model_score.points) + '%' ,
                'brief_comment': model_score.star_rating.comment,
                'detailed_comment': comments,
                'rating_changed_date': model_score.updated_date.strftime('%d/%m/%Y') + change_in_star_rating,
                'company_in_watch_list': 'true' if company_in_watch_list else 'false',
                'company_in_compare_list': 'true' if company_in_compare_list else 'false',
                'star_count': int(model_score.star_rating.star_count) if model_score.star_rating else 0,
                'change': int(model_score.star_rating_change) if model_score.star_rating_change else 0 ,
                'pricing': pricing
            })
    watch_list_count = 0
    compare_list_count = 0
    if public_user.count() > 0:
        watch_list = public_user[0].watchlist_set.all()
        compare_list = public_user[0].comparelist_set.all()
        watch_list_count = watch_list.count()
        compare_list_count = compare_list.count()
    response = simplejson.dumps({
        'star_ratings': ratings,
        'isin_list': isin_list,
        'watch_list_count': watch_list_count,
        'compare_list_count': compare_list_count,
        'total_count': total_count
    })
    return response

def get_rating_report(request, search_keys):
    ratings = []
    isin_list = []
    watch_list_companies_count = 0
    compare_list_companies_count = 0
    if request.user.is_authenticated():
        public_user = PublicUser.objects.filter(user=request.user)
        if public_user.count() > 0:
            watch_list_companies = public_user[0].watchlist_set.all()
            compare_list_companies = public_user[0].comparelist_set.all()
            watch_list_companies_count = watch_list_companies.count()
            compare_list_companies_count = compare_list_companies.count()
    for key in search_keys:
        company_in_watch_list = False
        company_in_compare_list = False
        company = Company.objects.get(isin_code=key)
        if company.is_all_data_available:
            if request.user.is_authenticated() and public_user.count() > 0:
                try:
                    watch_list = WatchList.objects.get(company=company, user=public_user[0])
                    company_in_watch_list = True
                except:
                    company_in_watch_list = False
                try:
                    compare_list = CompareList.objects.get(company=company, user=public_user[0])
                    company_in_compare_list = True
                except:
                    company_in_compare_list = False
            isin_list.append(company.isin_code)
            model_score = CompanyModelScore.objects.filter(company=company)
            if model_score.count() > 0:
                model_score = model_score[0]
                rating = {
                    'company_name': company.company_name + ' - ' + company.isin_code,
                    'bse_scrip_id': company.bse_scrip_id,
                    'bse_code': company.BSE_code,
                    'isin_code': company.isin_code,
                    'industry': company.industry.industry_name,
                    'star_rating': "*" * int(model_score.star_rating.star_count) if model_score.star_rating else '',
                    'score': model_score.points,
                    'brief_comment': model_score.star_rating.comment if model_score.star_rating else '',
                    'company_in_watch_list': 'true' if company_in_watch_list else 'false',
                    'company_in_compare_list': 'true' if company_in_compare_list else 'false',
                    'star_count': int(model_score.star_rating.star_count) if model_score.star_rating else 0,
                }
                model = model_score.analysis_model
                comments = []            
                analytical_heads = []
                for analytical_head in model.analytical_heads.all():
                    functions_details = []
                    for function in analytical_head.function_set.all().order_by('order'):
                        try:
                            parameter = ParameterLimit.objects.get(analysis_model=model, function=function)
                            fun_score = CompanyModelFunctionPoint.objects.filter(company=company, parameter_limit=parameter)
                            comment = ''
                            if fun_score.count() > 0:
                                fun_score = fun_score[0]
                                if fun_score.points == parameter.strong_points:
                                    comment = parameter.strong_comment
                                    comments.append(comment)
                                elif fun_score.points == parameter.weak_points:
                                    comment = parameter.weak_comment
                                    comments.append(comment)
                                elif fun_score.points == parameter.neutral_points:
                                    comment = parameter.neutral_comment
                                    comments.append(comment)  
                            function_score = CompanyFunctionScore.objects.filter(function=function, company=company)
                            if function_score.count() > 0:
                                function_score = function_score[0]
                                if function_score.score is not None:
                                    if analytical_head.title != 'Valuation' and parameter.function.function_name != 'Debt to Equity' :
                                        score = str(round(function_score.score, 2))+'%'
                                    else:
                                        score = round(function_score.score, 2)
                                else:
                                    function_score = None
                            else:
                                score = None
                                function_score = None
                            if comment:
                                functions_details.append({
                                    'function_name': function.function_name + (str(' - ') + str(score) if score is not None else ''),
                                    'score': score,
                                    'description': function.description,
                                    'comments': comment,
                                })
                        except:
                            pass

                    analytical_heads.append({
                        'analytical_head_name': analytical_head.title,
                        'functions': functions_details,
                    })
                rating['analytical_heads'] = analytical_heads
                rating['detailed_comment'] = comments
                pricing = {}
                try:
                    price = NSEBSEPrice.objects.get(company=company, latest=True)
                    last_review = NSEBSEPrice.objects.filter(company=company, last_review=True)[0]                
                    last_bse_price = last_review.BSE_price
                    last_nse_price = last_review.NSE_price
                    bse_change = ((last_bse_price - price.BSE_price)/price.BSE_price)*100
                    nse_change = ((last_nse_price - price.NSE_price)/price.NSE_price)*100
                    print 'up by '+str(round(abs(bse_change), 2))+ '% since last review' if bse_change>0 else  'down by '+str(round(abs(bse_change), 2))+ '% since last review',
                    pricing = {
                        'nse_price': price.NSE_price,
                        'bse_price': price.BSE_price,
                        'date': price.date.strftime('%d %B %Y'),
                        'bse_change': 'up by '+str(round(abs(bse_change), 2))+ '% since last review' if bse_change>0 else  'down by '+str(round(abs(bse_change), 2))+ '% since last review',
                        'nse_change': 'up by '+str(round(abs(nse_change), 2))+ '% since last review' if nse_change>0 else  'down by '+str(round(abs(nse_change), 2))+ '% since last review'
                    }
                except Exception as ex:
                    print str(ex)
                    pass
                rating['pricing'] = pricing
            else:
                rating = {
                    'company_name': company.company_name + ' - ' + company.isin_code,
                    'star_rating': 'Data not available' if not company.is_all_data_available else 'No Rating available'
                }
            ratings.append(rating)
    
    response = simplejson.dumps({
        'star_ratings': ratings,
        'isin_list': isin_list,
        'watch_list_count': watch_list_companies_count,
        'compare_list_count': compare_list_companies_count,
    })
    return response

def get_company_details(request):

    if request.GET.get('search_key', ''):
        companies = Company.objects.filter(company_name__istartswith=request.GET.get('search_key', ''), is_all_data_available=True)
    else:
        companies = Company.objects.filter(is_all_data_available=True)
    company_list = []
    for company in companies:
        company_list.append({
            'name': company.company_name,
            'isin_code': company.isin_code,
            'industry': company.industry.industry_name if company.industry else '',
            'created_by': company.created_by.username if company.created_by else '',
            'created_date': company.created_date.strftime("%d/%m/%Y")
        })
    response = simplejson.dumps({
        'result': 'Ok',
        'companies': company_list,
    })
    return response