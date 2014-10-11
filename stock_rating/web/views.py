
import simplejson
import ast
import lxml.etree as ET

from collections import OrderedDict
from math import sqrt

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

from models import (UserPermission, DataField, AnalyticalHead, Function,\
 ContinuityFunction, ConsistencyFunction, Industry, AnalysisModel, ParameterLimit, DataFile, \
 FieldMap, Operator, Company, CompanyFile, Formula, CompanyFunctionScore, CompanyModelScore, \
 StarRating, CompanyModelFunctionPoint)

from utils import process_data_file, process_company_file, \
    calculate_general_function_score, get_file_fields, calculate_consistency_function_score, \
    calculate_continuity_function_score

class Dashboard(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'dashboard.html', context)

class Administration(View):
    def get(self, request, *args, **kwargs):        
        context = {}
        return render(request, 'administration.html', context)

class FieldsWithMapping(View):
    def get(self, request, *args, **kwargs):
        field_objects = DataField.objects.all()
        fields = []
        if request.is_ajax():
            for field in field_objects:
                try:
                    f = FieldMap.objects.get(data_field=field)
                    fields.append({
                        'id': field.id,
                        'name': field.name,
                    })
                except:
                    continue
            response = simplejson.dumps({
                'result': 'OK',
                'fields': fields
            })
            return HttpResponse(response, status=200, mimetype='application/json')

class FieldSettings(View):
    def get(self, request, *args, **kwargs):
        field_objects = DataField.objects.all()
        fields = []
        for field in field_objects:
            if field.created_date.strftime("%d/%m/%Y") < field.updated_date.strftime("%d/%m/%Y"):
                status = "Modified"
                date = field.updated_date
            else:
                status = "Created"
                date = field.created_date
            fields.append({
                'id': field.id,
                'name': field.name,
                'description': field.description,
                'status': status,
                'date': date.strftime("%d/%m/%Y"),
            })
        if request.is_ajax():            
            response = simplejson.dumps({
                'result': 'OK',
                'fields': fields
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        context = {}
        return render(request, 'field_settings.html', context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            field_details = ast.literal_eval(request.POST['field_details'])
            try:
                field = DataField.objects.get(id=field_details['id'])
            except:
                field = DataField()
            field.name = field_details['field_name']
            field.description = field_details['field_description']
            field.created_by = request.user
            try:
                field.save()
                res = {
                  'result': 'ok',
                }
            except:
                res = {
                  'result': 'error',  
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'field_settings.html', {})

class FunctionSettings(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            function_objects = Function.objects.all()
            functions = []
            for function in function_objects:
                functions.append({
                        'id': function.id,
                        'name': function.function_name,
                        'head': function.analytical_head.title,
                        # 'category': function.category.category_name,
                        'created_date': function.created_date.strftime("%d/%m/%Y"),
                        'modified_date': function.updated_date.strftime("%d/%m/%Y"),
                        'function_type': function.function_type,
                    })
            if request.is_ajax():
                response = simplejson.dumps({
                    'result': 'OK',
                    'functions': functions
                })
                return HttpResponse(response, status=200, mimetype='application/json')
        context = {}
        return render(request, 'function_settings.html', context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            function_details = ast.literal_eval(request.POST['function_details'])
            function_type = ast.literal_eval(request.POST['function_type'])
            if int(function_type) == 1:
                operators = ast.literal_eval(request.POST['formula_operators'])
                operands = ast.literal_eval(request.POST['formula_operands'])
                formula_string = request.POST['formula_string']
                try:
                    general_function = Function.objects.get(id=function_details['id'])
                    if general_function.formula:
                        general_function.formula.operands.clear()
                        general_function.formula.operators.clear()
                        general_function.formula.save()
                        general_function.save()
                except:
                    general_function = Function()
                anly_head = AnalyticalHead.objects.get(id=function_details['select_head'])
                general_function.function_name = function_details['function_name']
                general_function.description = function_details['function_description']
                general_function.function_type = 'general'
                general_function.analytical_head = anly_head
                general_function.save()
                formula = Formula.objects.create(formula_string=formula_string)
                for operator in operators:
                    op = Operator.objects.get(id=int(operator['id']))
                    formula.operators.add(op)
                for operand in operands:
                    opnd = DataField.objects.get(id=operand['id'])
                    formula.operands.add(opnd)
                formula.save()
                general_function.formula = formula
                general_function.save()
                res = {
                  'result': 'ok',
                }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
            elif int(function_type) == 2:
                try:
                    continuity_function = ContinuityFunction.objects.get(id=function_details['id'])
                except:
                    continuity_function = ContinuityFunction()
                anly_head = AnalyticalHead.objects.get(id=function_details['select_head'])
                continuity_function.function_name = function_details['function_name']
                continuity_function.description = function_details['function_description']
                continuity_function.function_type = 'continuity'
                continuity_function.analytical_head = anly_head
                continuity_function.number_of_fields = function_details['no_of_fields']
                continuity_function.number_of_functions = function_details['no_of_functions']
                try:
                    continuity_function.save()
                    if continuity_function.fields:
                        continuity_function.fields.clear()
                    fields = function_details['fields']
                    for field in fields:
                        datafield = DataField.objects.get(id=int(field['field']))
                        continuity_function.fields.add(datafield)
                    if continuity_function.functions:
                        continuity_function.functions.clear()
                    functions = function_details['functions']
                    for function in functions:
                        datafunction = Function.objects.get(id=int(function['function']))
                        continuity_function.functions.add(datafunction)
                    res = {
                      'result': 'ok',
                    }
                except Exception as ex:
                    res = {
                      'result': 'error',  
                      'message': str(ex)
                    }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
            elif int(function_type) == 3:
                try:
                    consistency_function = ConsistencyFunction.objects.get(id=function_details['id'])
                except:
                    consistency_function = ConsistencyFunction()
                anly_head = AnalyticalHead.objects.get(id=function_details['select_head'])
                consistency_function.function_name = function_details['function_name']
                consistency_function.description = function_details['function_description']
                consistency_function.function_type = 'consistency'
                consistency_function.analytical_head = anly_head
                consistency_function.number_of_fields = function_details['no_of_fields']
                consistency_function.number_of_functions = function_details['no_of_functions']
                try:
                    consistency_function.save()
                    if consistency_function.fields:
                        consistency_function.fields.clear()
                    fields = function_details['fields']
                    for field in fields:
                        datafield = DataField.objects.get(id=int(field['field']))
                        consistency_function.fields.add(datafield)
                    if consistency_function.functions:
                        consistency_function.functions.clear()
                    functions = function_details['functions']
                    for function in functions:
                        datafunction = Function.objects.get(id=int(function['function']))
                        consistency_function.functions.add(datafunction)
                    res = {
                      'result': 'ok',
                    }
                except Exception as ex:
                    res = {
                      'result': 'error',  
                      'message': str(ex)
                    }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'function_settings.html', {})

class Companies(View):
    def get(self, request, *args, **kwargs):
        if request.GET.get('search_key', ''):
            companies = Company.objects.filter(company_name__istartswith=request.GET.get('search_key', ''))
        else:
            companies = Company.objects.all()
        company_files = CompanyFile.objects.all()
        if company_files.count() > 0:
            company_file = CompanyFile.objects.latest('id')
            if company_file.processing_completed:
                pass
            else:
                process_company_file(company_file)
        else:
            company_file = None
        if request.is_ajax():
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
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'companies.html', {
            'company_file': company_file,
            'status': ('Processing Completed' if company_file.processing_completed else 'Processing Pending') if company_file else '',
        })

    def post(self, request, *args, **kwargs):
        company_file  = CompanyFile()
        company_file.uploaded_file = request.FILES['data_file']
        company_file.uploaded_by = request.user
        company_file.save()    
        process_company_file(company_file)
        if request.is_ajax():
            response = simplejson.dumps({
               'result': 'OK',
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        context = {}
        return render(request, 'companies.html', context)

class DataUpload(View):
    def get(self, request, *args, **kwargs):
        data_files = DataFile.objects.all()
        if data_files.count() > 0:
            data_file = DataFile.objects.latest('id')
            d_files = DataFile.objects.filter(processing_completed=False)
            for d_file in d_files:        
                if d_file.processing_completed:
                    pass
                else:
                    process_data_file(d_file)
        else:
            data_file = None
        file_list = []
        if request.is_ajax():
            for data_file in data_files:
                file_list.append({
                    'id': data_file.id,
                    'uploaded_by': data_file.uploaded_by.username,
                    'uploaded_date': data_file.created_date.strftime('%d/%m/%Y'),
                    'path': data_file.uploaded_file.name
                })
            response = simplejson.dumps({
               'data_files': file_list,
            })
            return HttpResponse(response, status=200, mimetype='application/json')

        return render(request, 'data_upload.html', {
            'data_file': data_file,
            'status': ('Processing Completed' if data_file.processing_completed else 'Processing Pending') if data_file else '',
        })

    def post(self, request, *args, **kwargs):
            
        data_file = DataFile()
        data_file.uploaded_file = request.FILES['data_file']
        data_file.uploaded_by = request.user
        data_file.save()        
        sheets = process_data_file(data_file)
        data_file.sheets = sheets
        data_file.save()

        if request.is_ajax():
            response = simplejson.dumps({
               'sheets': sheets,
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        context = {}
        return render(request, 'data_upload.html', context)

class FieldMapping(View):
    def get(self, request, *args, **kwargs):
        total_file_fields = get_file_fields()
        mappings = FieldMap.objects.count()
        if mappings > 0:
            mapping_status = 'exists'
        else:
            mapping_status = 'empty'
        if request.is_ajax():
            mapping = FieldMap.objects.all()
            system_fields = []
            file_fields = []
            for mp in mapping:
                system_fields.append({
                    'id': mp.data_field.id if mp.data_field else '',
                    'name': mp.data_field.name if mp.data_field else '',  
                    'mapping_id': mp.id                  
                })
                file_fields.append(mp.file_field)
            for field in DataField.objects.all():
                try:
                    f = FieldMap.objects.get(data_field = field)
                except:
                    system_fields.append({
                        'id': field.id,
                        'name': field.name,  
                        'mapping_id': '' ,
                    })
            for field in total_file_fields:
                if field not in file_fields:
                    file_fields.append(field)
            response = simplejson.dumps({
                'result': 'Ok',
                'file_fields': file_fields,
                'system_fields': system_fields
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'field_mapping.html', {
            'mapping_status': mapping_status
        })

    def post(self, request, *args, **kwargs):
        data_file = DataFile.objects.latest('id')
        if request.is_ajax():
            system_fields = ast.literal_eval(request.POST['system_fields'])
            file_fields = ast.literal_eval(request.POST['file_fields'])
            mappings = FieldMap.objects.count()
            if mappings > 0:
                for system_field, file_field in zip(system_fields, file_fields):
                    if system_field['id'] != '':
                        system_field = DataField.objects.get(id=system_field['id'])
                    else:
                        system_field = None
                    try:
                        mapping = FieldMap.objects.get(id=system_field['mapping_id'])
                        mapping.system_field = system_field
                        mapping.file_field = file_field
                    except:
                        if file_field != '':
                            mapping, created = FieldMap.objects.get_or_create(data_field=system_field)
                            mapping.data_file = data_file
                            mapping.file_field = file_field 
                            mapping.save()
                    mapping.save()
            else:
                for system_field, file_field in zip(system_fields, file_fields):
                    if len(file_field.strip()) > 0:
                        if system_field['id'] != '':
                            system_field = DataField.objects.get(id=system_field['id'])
                        else:
                            system_field = None
                        mapping = FieldMap.objects.create(data_file=data_file, data_field=system_field, file_field=file_field)
                        mapping.save()
            response = simplejson.dumps({
                'result': 'Ok'
            })
            return HttpResponse(response, status=200, mimetype='application/json')

        return render(request, 'field_mapping.html', {})

class FileFields(View):
    def get(self, request, *args, **kwargs):
        file_obj = DataFile.objects.latest('id')
        if file_obj:
            if request.is_ajax():
                fields = []
                for sheet in file_obj.sheets:
                    if len(sheet['rows']) > 0:
                        fields.append(sheet['rows'][0])
                fields = [x for y in fields for x in y]
                response = simplejson.dumps({
                    'fields': list(OrderedDict.fromkeys(fields))
                })
                return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'field_mapping.html', {
            'fields' : file_obj.sheets if file_obj else []
        })

class AnalyticalHeads(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            head_objects = AnalyticalHead.objects.all()
            heads = []
            function_set = []
            for head in head_objects:
                if head.created_date.strftime("%d/%m/%Y") < head.updated_date.strftime("%d/%m/%Y"):
                    status = "Modified"
                    date = head.updated_date
                else:
                    status = "Created"
                    date = head.created_date
                function_list = head.function_set.all()
                for function in function_list:
                    function_set.append({
                        'function_id': function.id,
                        'function_name': function.function_name,
                    })
                heads.append({
                    'id':head.id,
                    'title': head.title,
                    'description': head.description,
                    'status': status,
                    'date': date.strftime("%d/%m/%Y"),
                    'function_set': function_set,
                })
                function_set = []
            if request.is_ajax():
                response = simplejson.dumps({
                   'head_objects': heads
                })
            return HttpResponse(response, status=200, mimetype='application/json')
        context = {}
        return render(request, 'analytical_heads.html', context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            head_details = ast.literal_eval(request.POST['head_details'])
            try:
                head = AnalyticalHead.objects.get(id=head_details['id'])
            except:
                head = AnalyticalHead()
            head.title = head_details['head_name']
            head.description = head_details['head_description']
            head.created_by = request.user
            try:
                head.save()
                res = {
                  'result': 'ok',
                }
            except:
                res = {
                  'result': 'error',  
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'analytical_heads.html', {})


class Model(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            analysis_model_objects = AnalysisModel.objects.all()
            analysis_models = []
            industry_set = []
            analytical_head_set = []
            for model in analysis_model_objects:
                industries = model.industries.all()
                analytical_heads = model.analytical_heads.all()
                for analytical_head in analytical_heads:
                    analytical_head_set.append({
                        'id': analytical_head.id,
                        'head': analytical_head.title,
                    })
                for industry in industries:
                    industry_set.append({
                        'id': industry.id,
                        'name': industry.industry_name,
                    })
                analysis_models.append({
                    'id':model.id,
                    'name': model.name,
                    'description': model.description,
                    'industry': industry_set,
                    'analytical_heads': analytical_head_set,
                    'created_date': model.created_date.strftime("%d/%m/%Y"),
                    'modified_date': model.updated_date.strftime("%d/%m/%Y"),
                })
                industry_set = []
                analytical_head_set = []
            if request.is_ajax():
                response = simplejson.dumps({
                   'model_list': analysis_models
                })
                return HttpResponse(response, status=200, mimetype='application/json')
        context = {}
        return render(request, 'models.html', context)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            model_details = ast.literal_eval(request.POST['model_details'])
            analytical_heads = ast.literal_eval(request.POST['analytical_heads'])
            industry_selected = ast.literal_eval(request.POST['industry_selected'])
            try:
                model = AnalysisModel.objects.get(id=model_details['id'])
            except:
                model = AnalysisModel()
            model.name = model_details['model_name']
            model.description = model_details['model_description']
            try:
                model.save()
                industry_remove =  model.industries.all()
                analytical_head_remove = model.analytical_heads.all()
                for industry in industry_remove:
                    model.industries.remove(industry.id)
                for analytical_head in analytical_head_remove:
                    model.analytical_heads.remove(analytical_head.id)
                for industry in industry_selected:
                    model.industries.add(industry)
                for head in analytical_heads:
                    if head['selected'] == "true":
                        model.analytical_heads.add(head['id'])
          
                res = {
                  'result': 'ok',
                }
            except:
                res = {
                  'result': 'error',  
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'models.html', {})


class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {})

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'login.html', context)     

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class Users(View):

    def get(self, request, *args, **kwargs):
        user_objects = User.objects.all()
        users = []
        for user in user_objects:
            if user.userpermission_set.all().count():
                permission = user.userpermission_set.all()[0]
            else:
                permission = None
            if not user.is_superuser:
                users.append({
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'password': user.password,
                    'data_upload': permission.data_upload if permission else False,
                    'field_settings': permission.field_settings if permission else False,
                    'score_settings': permission.score_settings if permission else False,
                    'function_settings': permission.function_settings if permission else False,
                    'analytical_heads': permission.analytical_heads if permission else False
                })
        if request.is_ajax():
            response = simplejson.dumps({
                'result': 'OK',
                'users': users
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'administration.html', {
            'users': user_objects
        })

class IndustryDetails(View):

    def get(self, request, *args, **kwargs):
        industry_objects = Industry.objects.all()
        industry_list = []
        for industry in industry_objects:
            industry_list.append({
                    'id': industry.id,
                    'name': industry.industry_name,
                })
        if request.is_ajax():
            response = simplejson.dumps({
                'result': 'OK',
                'industry_list': industry_list
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'models.html', {
           
        })


class SaveUser(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            user_details = ast.literal_eval(request.POST['user_details'])
            if user_details['id'] != '':
                user = User.objects.get(id=user_details['id'])
                permission = UserPermission.objects.get(user=user)
            else:
                permission = UserPermission()
                user = User()
            user.username = user_details['username']
            user.first_name = user_details['first_name']
            if user_details['password']:
                user.set_password(user_details['password'])
            try:
                user.save()            
                permission.user = user
                permission.data_upload = True if user_details['data_upload'] == "true" else False
                permission.field_settings = True if user_details['field_settings'] == "true" else False
                permission.score_settings = True if user_details['score_settings'] == "true" else False
                permission.function_settings = True if user_details['function_settings'] == "true" else False
                permission.analytical_heads = True if user_details['analytical_heads'] == "true" else False
                permission.save()
                res = {
                    'result': 'ok',
                }
            except:
                res = {
                    'result': 'error',
                }

            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'administration.html', {})


class ModelDetails(View):
    def get(self, request, *args, **kwargs):
        model = AnalysisModel.objects.get(id=request.GET.get('id'))
        parameter_set = {}
        function_set = []
        empty_functions = []
        analytical_head_set = []
        analytical_heads_list =  model.analytical_heads.all()
        star_ratings = model.starrating_set.all()
        for analytical_head in analytical_heads_list:
            function_list = analytical_head.function_set.all()
            for function in function_list:
                parameter_list = ParameterLimit.objects.filter(analysis_model_id=model.id, function_id=function.id)
                if parameter_list.count() == 0:
                    empty_functions.append({
                        'name': function.function_name,
                        'id': function.id
                    })
                for parameter in parameter_list:
                    parameter_set = {
                        'parameter_id': parameter.id,
                        'strong_min': parameter.strong_min,
                        'strong_max': parameter.strong_max,
                        'strong_points': parameter.strong_points,
                        'neutral_min': parameter.neutral_min,
                        'neutral_max': parameter.neutral_max,
                        'neutral_points': parameter.neutral_points,
                        'weak_min': parameter.weak_min,
                        'weak_max': parameter.weak_max,
                        'weak_points': parameter.weak_points,
                        'weak_min_1': parameter.weak_min_1 if parameter.weak_min_1 is not None else '',
                        'weak_max_1': parameter.weak_max_1 if parameter.weak_max_1 is not None else '',
                        'strong_comment': parameter.strong_comment,
                        'weak_comment': parameter.weak_comment,
                        'neutral_comment': parameter.neutral_comment
                    }
                    function_set.append({
                        'function_id':function.id,
                        'function_name': function.function_name,     
                        'parameter_set': parameter_set,
                    })
                    parameter_set = {}
            ratings = []
            for rating in star_ratings:
                ratings.append({
                    'id': rating.id,
                    'star_count': rating.star_count,
                    'min_score': rating.min_score,
                    'max_score': rating.max_score,
                    'comment': rating.comment
                })
            analytical_head_set.append({
                'analytical_head_id': analytical_head.id,
                'analytical_head_name': analytical_head.title,
                'function_set': function_set,
                'empty_functions': empty_functions,
            })
            function_set = []
            empty_functions = []
        if request.is_ajax():
            response = simplejson.dumps({
                'analytical_heads': analytical_head_set,
                'star_ratings': ratings,
            })
        return HttpResponse(response, status=200, mimetype='application/json')

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            model_id = ast.literal_eval(request.POST['model_id'])
            parameters = ast.literal_eval(request.POST['parameters'])
            try:
                parameterlimit = ParameterLimit.objects.get(id=parameters['parameter_id'])
            except:
                parameterlimit = ParameterLimit()
                function_id = ast.literal_eval(request.POST['function_id'])
                analysis_model = AnalysisModel.objects.get(id=model_id)
                function = Function.objects.get(id=function_id)
                parameterlimit.analysis_model = analysis_model
                parameterlimit.function = function
            parameterlimit.strong_min = parameters['strong_min']
            parameterlimit.strong_max = parameters['strong_max']
            parameterlimit.strong_points = parameters['strong_points']
            parameterlimit.neutral_min = parameters['neutral_min']
            parameterlimit.neutral_max = parameters['neutral_max']
            parameterlimit.neutral_points = parameters['neutral_points']
            parameterlimit.weak_min = parameters['weak_min']
            parameterlimit.weak_max = parameters['weak_max']
            parameterlimit.weak_points = parameters['weak_points'] 
            if len(str(parameters['weak_min_1'])) > 0:
                parameterlimit.weak_min_1 = parameters['weak_min_1']
            else:
                parameterlimit.weak_min_1 = None
            if len(str(parameters['weak_max_1'])) > 0:
                parameterlimit.weak_max_1 = parameters['weak_max_1']
            else:
                parameterlimit.weak_max_1 = None
            parameterlimit.strong_comment = parameters['strong_comment']
            parameterlimit.weak_comment = parameters['weak_comment']
            parameterlimit.neutral_comment = parameters['neutral_comment']
            try:
                parameterlimit.save()
                res = {
                  'result': 'ok',
                }
            except:
                res = {
                  'result': 'error',  
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'models.html', {})


class GeneralFunctions(View):

    def get(self, request, *args, **kwargs):
        general_function = Function.objects.get(id=request.GET.get('id'))
        formula_operators = []
        formula_operands = []
        if general_function.formula:
            for operator in general_function.formula.operators.all().all():
                formula_operators.append({
                    'id': operator.id,
                    'symbol': operator.symbol
                })
            for operand in general_function.formula.operands.all().all():
                formula_operands.append({
                    'id': operand.id,
                    'name': operand.name,
                })
        general_dict = {
            'id':general_function.id,
            'name': general_function.function_name,
            'description': general_function.description,
            'head': general_function.analytical_head.id,
            'formula': general_function.formula.formula_string if general_function.formula else '',
            # 'category': general_function.category.id,
            'formula_operands': formula_operands,
            'formula_operators': formula_operators
        }
        if request.is_ajax():
            response = simplejson.dumps({
               'general_function': general_dict
            })
        return HttpResponse(response, status=200, mimetype='application/json')


class ContinuityFunctions(View):

    def get(self, request, *args, **kwargs):
        continuity_objects = ContinuityFunction.objects.get(id=request.GET.get('id'))
        continuity_set = []
        field_set = []
        fields = continuity_objects.fields.all()       
        for field in fields:
            field_set.append({
                'field': field.id,
            })
        function_set = []
        functions = continuity_objects.functions.all()       
        for function in functions:
            function_set.append({
                'function': function.id,
            })    
        continuity_fucntion = {
            'id':continuity_objects.id,
            'function_name': continuity_objects.function_name,
            'function_description': continuity_objects.description,
            'select_head': continuity_objects.analytical_head.id,
            'no_of_fields': continuity_objects.number_of_fields, 
            'no_of_functions': continuity_objects.number_of_functions,              
            'fields': field_set,
            'functions': function_set
        }
        if request.is_ajax():
            response = simplejson.dumps({
               'continuity_fucntion': continuity_fucntion
            })
            return HttpResponse(response, status=200, mimetype='application/json')


class ConsistencyFunctions(View):

    def get(self, request, *args, **kwargs):
        consistency_objects = ConsistencyFunction.objects.get(id=request.GET.get('id'))
        field_set = []
        function_set = []
        fields = consistency_objects.fields.all()       
        for field in fields:
            field_set.append({
                'field': field.id,
            })
        functions = consistency_objects.functions.all()       
        for function in functions:
            function_set.append({
                'function': function.id,
            })
        consistency_function = {
            'id':consistency_objects.id,
            'function_name': consistency_objects.function_name,
            'function_description': consistency_objects.description,
            'select_head': consistency_objects.analytical_head.id,
            'no_of_fields': consistency_objects.number_of_fields, 
            'no_of_functions': consistency_objects.number_of_functions,              
            'fields': field_set,
            'functions': function_set,
        }
        if request.is_ajax():
            response = simplejson.dumps({
               'consistency_function': consistency_function
            })
            return HttpResponse(response, status=200, mimetype='application/json')


class DeleteField(View):
    def get(self, request, *args, **kwargs):
        field = DataField.objects.get(id=request.GET.get('id')) 
        if field.formula_set.all().count() == 0:
            field.delete()
            res = {
              'result': 'ok',
            }
        else:
            res = {
               'result': 'error',  
               'message': 'This field is used in funtion Formula'
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class DeleteHead(View):
    def get(self, request, *args, **kwargs):
        head = AnalyticalHead.objects.get(id=request.GET.get('id'))        
        if head.analysismodel_set.all().count() == 0:
            head.delete()
            res = {
                'result': 'ok',
            }
        else:
            res = {
                'result': 'error',  
                'message': 'This head is used in one of the models'
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class DeleteModel(View):
    def get(self, request, *args, **kwargs):
        model = AnalysisModel.objects.get(id=request.GET.get('id')) 
        try:
            model.delete()
            res = {
              'result': 'ok',
            }
        except:
            res = {
               'result': 'error',  
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.GET.get('id')) 
        try:
            user.delete()
            res = {
              'result': 'ok',
            }
        except:
            res = {
               'result': 'error',  
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class DeleteParameter(View):
    def get(self, request, *args, **kwargs):
        parameterlimit = ParameterLimit.objects.get(id=request.GET.get('id'))
        try:
            parameterlimit.delete()
            res = {
              'result': 'ok',
            }
        except:
            res = {
               'result': 'error',  
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')


class DeleteRating(View):
    def get(self, request, *args, **kwargs):
        star_rating = StarRating.objects.get(id=request.GET.get('rating_id'))       
        try:
            star_rating.delete()
            res = {
              'result': 'ok',
            }
        except:
            res = {
               'result': 'error',  
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')


class ResetPassword(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            if request.POST['id'] != '':
                user = User.objects.get(id=request.POST['id'])
            user.set_password(request.POST['password'])
            user.save()
            res = {
                'result': 'ok',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'administration.html', {})

class OperatorsView(View):

    def get(self, request, *args, **kwargs):
        operators = Operator.objects.all()

        if request.is_ajax():
            op_list = []
            for operator in operators:
                op_list.append({
                    'id': operator.id,
                    'symbol': operator.symbol
                })
            res = {
                'result': 'ok',
                'operators': op_list
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'administration.html', {
            'operators': operators
        })

class DeleteFunction(View):
    def get(self, request, *args, **kwargs):
        function = Function.objects.get(id=kwargs['function_id'])
        function.delete()
        return HttpResponseRedirect(reverse('function_settings'))

class DeleteDataFile(View):
    def get(self, request, *args, **kwargs):
        data_file = DataFile.objects.get(id=kwargs['file_id'])
        data_file.delete()
        return HttpResponseRedirect(reverse('data_upload'))

class ModelStarRating(View):
    def get(self, request, *args, **kwargs):
        model = AnalysisModel.objects.get(id=kwargs['model_id'])
        industries = model.industries.all()
        model_max_point = 0
        parameterlimits = ParameterLimit.objects.filter(analysis_model=model)
        for parameterlimit in parameterlimits:
            function = parameterlimit.function
            model_max_point = model_max_point + parameterlimit.strong_points  
        model.max_points = model_max_point
        model.save()
        model_ratings = model.starrating_set.all() 
        parameterlimits = ParameterLimit.objects.filter(analysis_model=model)
        for industry in industries:
            companies = industry.company_set.all()
            for company in companies:
                if not company.is_all_data_available:
                    continue
                model_point = 0
                score = 0
                company_model_score, created = CompanyModelScore.objects.get_or_create(company=company, analysis_model=model)
                
                for parameterlimit in parameterlimits:
                    function = parameterlimit.function
                    try:
                        if function.function_type == 'general':
                            calculate_general_function_score(function, company)
                        elif function.function_type == 'consistency':
                            calculate_consistency_function_score(function, company)
                        elif function.function_type == 'continuity':
                            calculate_continuity_function_score(function, company)
                        function_score = CompanyFunctionScore.objects.get(company=company, function=function)
                        company_model_function_point, created  = CompanyModelFunctionPoint.objects.get_or_create(company=company, function=function, model=model)
                        if not parameterlimit.strong_max.replace('.','',1).replace('-','',1).isdigit() and function_score.score >= float(parameterlimit.strong_min):
                            company_model_function_point.points = parameterlimit.strong_points
                            company_model_function_point.comment = parameterlimit.strong_comment
                            company_model_function_point.save()                               
                        elif function_score.score >= float(parameterlimit.strong_min) and function_score.score < float(parameterlimit.strong_max):
                            company_model_function_point.points = parameterlimit.strong_points                                
                            company_model_function_point.comment = parameterlimit.strong_comment
                            company_model_function_point.save()
                        elif function_score.score >= float(parameterlimit.neutral_min) and function_score.score < float(parameterlimit.neutral_max):
                            company_model_function_point.points = parameterlimit.neutral_points
                            company_model_function_point.comment = parameterlimit.neutral_comment
                            company_model_function_point.save()
                        elif not parameterlimit.weak_min.replace('.','',1).replace('-','',1).isdigit() and function_score.score < float(parameterlimit.weak_max):
                            company_model_function_point.points = parameterlimit.weak_points
                            company_model_function_point.comment = parameterlimit.weak_comment
                            company_model_function_point.save()
                        elif not parameterlimit.weak_max.replace('.','',1).replace('-','',1).isdigit() and function_score.score >= float(parameterlimit.weak_min):
                            company_model_function_point.points = parameterlimit.weak_points
                            company_model_function_point.comment = parameterlimit.weak_comment
                            company_model_function_point.save()
                        elif function_score.score >= float(parameterlimit.weak_min) and function_score.score < float(parameterlimit.weak_max):
                            company_model_function_point.points = parameterlimit.weak_points
                            company_model_function_point.comment = parameterlimit.weak_comment
                            company_model_function_point.save()
                        elif parameterlimit.weak_min_1 is not None:
                            if not parameterlimit.weak_min_1.replace('.','',1).replace('-','',1).isdigit():
                                if function_score.score < float(parameterlimit.weak_max_1):
                                    company_model_function_point.points = parameterlimit.weak_points
                                    company_model_function_point.comment = parameterlimit.weak_comment
                                    company_model_function_point.save()
                            elif not parameterlimit.weak_max_1.replace('.','',1).replace('-','',1).isdigit():
                                if parameterlimit.weak_max_1 == "Above":
                                    if function_score.score >= float(parameterlimit.weak_min_1):
                                        company_model_function_point.points = parameterlimit.weak_points
                                        company_model_function_point.comment = parameterlimit.weak_comment
                                        company_model_function_point.save()
                                elif parameterlimit.weak_max_1 == "Below":
                                    if function_score.score < float(parameterlimit.weak_min_1):
                                        company_model_function_point.points = parameterlimit.weak_points
                                        company_model_function_point.comment = parameterlimit.weak_comment
                                        company_model_function_point.save()
                            elif function_score.score >= float(parameterlimit.weak_min_1) and function_score.score < float(parameterlimit.weak_max_1):
                                company_model_function_point.points = parameterlimit.weak_points
                                company_model_function_point.comment = parameterlimit.weak_comment
                                company_model_function_point.save()                                    
                        score = score + function_score.score
                        model_point = model_point + company_model_function_point.points
                    except Exception as e:
                        continue
                company_model_score.score = score
                point = float(model_point)/float(model.max_points)*100
                round_function = lambda point: int(point + 1) if int(point) != point else int(point)
                company_model_score.points = round_function(point)
                company_model_score.save()
                for rating in model_ratings:
                    if company_model_score.points >= rating.min_score and company_model_score.points <= rating.max_score:
                        company_model_score.star_rating = rating.star_count
                        company_model_score.comment = rating.comment
                        company_model_score.save()
                        break;
                    elif rating.star_count == 5:
                        if company_model_score.points >= rating.min_score:
                            company_model_score.star_rating = rating.star_count
                            company_model_score.comment = rating.comment
                            company_model_score.save()
                            break;
        response = simplejson.dumps({
            'result': 'OK'
        })
        return HttpResponse(response, status=200, mimetype='application/json')


class SaveModelStarRating(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            rating_details = ast.literal_eval(request.POST['rating'])
            if rating_details['id']:
                rating = StarRating.objects.get(id=rating_details['id'])
            else:
                model = AnalysisModel.objects.get(id=kwargs['model_id'])
                rating = StarRating()
                rating.model = model
            rating.star_count = rating_details['star_count']
            rating.min_score = rating_details['min_score']
            if rating_details['max_score']:
                rating.max_score = rating_details['max_score']
            else:
                rating.max_score = None
            rating.comment = rating_details['comment']
            rating.save()
        return HttpResponseRedirect(reverse("models"))

class RatingReport(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'rating_report.html', {
            
        })
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            search_keys = ast.literal_eval(request.POST['search_keys'])
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
                    rating['detailed_comment'] = comments
                else:
                    rating = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'star_rating': 'Data not available' if not company.is_all_data_available else 'No Rating available'
                    }
                ratings.append(rating)
            response = simplejson.dumps({
                'star_ratings': ratings,
                'isin_list': isin_list
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'rating_report.html', {})
            
class RatingReportByStarCount(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'rating_report.html', {
            
        })
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            star_count = ast.literal_eval(request.POST['star_count'])
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
                    'industry': company.industry.industry_name,
                    'star_rating': "*" * int(model_score.star_rating) if model_score.star_rating else '',
                    'score': model_score.points,
                    'brief_comment': model_score.comment,
                    'detailed_comment': comments
                })
            response = simplejson.dumps({
                'star_ratings': ratings,
                'isin_list': isin_list
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'rating_report.html', {})

class RatingXML(View):
    
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            isin_list = ast.literal_eval(request.POST['isin_list'])
            root = ET.Element("ratings")
            for code in isin_list:
                company = Company.objects.get(isin_code=code)
                model_score = CompanyModelScore.objects.filter(company=company)
                if model_score.count() > 0:
                    model_score = model_score[0]
                    doc = ET.SubElement(root, "rating")

                    field1 = ET.SubElement(doc, "company_name")
                    field1.text = company.company_name

                    field2 = ET.SubElement(doc, "isin_code")
                    field2.text = company.isin_code

                    field3 = ET.SubElement(doc, "industry")
                    field3.text = company.industry.industry_name
                    field4 = ET.SubElement(doc, "star_rating")
                    field4.text = model_score.star_rating
                    field5 = ET.SubElement(doc, "score")
                    field5.text = str(model_score.points)
                    field6 = ET.SubElement(doc, "brief_comment")
                    field6.text = model_score.comment

                    model = model_score.analysis_model
                    parameters = model.parameterlimit_set.all()
                    comments = []
                    for parameter in parameters:
                        function = parameter.function
                        fun_score = CompanyModelFunctionPoint.objects.filter(company=company, function=function, model=model)
                        if fun_score.count() > 0:
                            if fun_score[0].comment:
                                comments.append(fun_score[0].comment)
                    field6 = ET.SubElement(doc, "detailed_comment")
                    field6.text = ', '.join(comments)
                else:
                    doc = ET.SubElement(root, "rating")
                    doc.text = 'Data not available' if not company.is_all_data_available else 'No Rating available'
            tree = ET.ElementTree(root)
            tree.write(settings.MEDIA_ROOT+"/rating.xml")
            response = simplejson.dumps({
                'file_name': "rating.xml"
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'rating_report.html', {})