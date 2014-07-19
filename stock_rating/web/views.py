
import simplejson
import ast
import re

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from models import UserPermission, DataField, FunctionCategory, AnalyticalHead, Function, ContinuityFunction, ConsistencyFunction, Industry, AnalysisModel

class Dashboard(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'dashboard.html', context)

class Administration(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'administration.html', context)


class FieldSettings(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'field_settings.html', context)


class FunctionSettings(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'function_settings.html', context)


class Model(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'models.html', context)


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

class Category(View):

    def get(self, request, *args, **kwargs):
        item_list = FunctionCategory.objects.all()
        items = []
        for item in item_list:
            items.append({
                'id':item.id,
                'category': item.category_name
            })
        if request.is_ajax():
            response = simplejson.dumps({
               'item_list': items
            })
            return HttpResponse(response, status=200, mimetype='application/json')


class ModelDetails(View):

    def get(self, request, *args, **kwargs):
        item_list = AnalysisModel.objects.all()
        items = []
        industry_set = []
        for item in item_list:
            industries = item.industries.all()
            for industry in industries:
                industry_set.append({
                    'id': industry.id,
                    'name': industry.industry_name,
                })
            #print industry_set
            items.append({
                'id':item.id,
                'name': item.name,
                'description': item.description,
                'industry': industry_set,
                'created_date': item.created_date.strftime("%d/%m/%Y"),
                'modified_date': item.updated_date.strftime("%d/%m/%Y"),
            })
            industry_set = []
        if request.is_ajax():
            response = simplejson.dumps({
               'model_list': items
            })
            return HttpResponse(response, status=200, mimetype='application/json')


class Analyt_Heads(View):

    def get(self, request, *args, **kwargs):
        item_list = AnalyticalHead.objects.all()
        items = []
        for item in item_list:
            items.append({
                'id':item.id,
                'title': item.title
            })
        if request.is_ajax():
            response = simplejson.dumps({
               'item_list': items
            })
            return HttpResponse(response, status=200, mimetype='application/json')

class Fields(View):

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
        return render(request, 'field_settings.html', {
            'fields': field_objects
        })


class Functions(View):

    def get(self, request, *args, **kwargs):
        function_objects = Function.objects.all()
        functions = []
        category_list = []
        for function in function_objects:
            functions.append({
                    'id': function.id,
                    'name': function.function_name,
                    'head': function.analytical_head.title,
                    'category': function.category.category_name,
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
        return render(request, 'function_settings.html', {
           
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
            user.save()
            user.set_password(user_details['password'])
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
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'administration.html', {})


class SaveField(View):
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


class SaveModel(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            model_details = ast.literal_eval(request.POST['model_details'])
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
                print industry_remove
                for industry in industry_remove:
                    model.industries.remove(industry.id)
                for industry in industry_selected:
                    model.industries.add(industry)
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


class SaveFunction(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            function_details = ast.literal_eval(request.POST['function_details'])
            function_type = ast.literal_eval(request.POST['function_type'])
            function_category = ast.literal_eval(request.POST['function_category'])
            category=FunctionCategory.objects.get(id=function_category)
            if int(function_type) == 1:
                try:
                    general_function = Function.objects.get(id=function_details['id'])
                except:
                    general_function = Function()
                # general_function.category = function_category
                anly_head = AnalyticalHead.objects.get(id=function_details['select_head'])
                general_function.category = category
                general_function.function_name = function_details['function_name']
                general_function.description = function_details['function_description']
                general_function.function_type = 'general'
                general_function.analytical_head = anly_head
                # formula_list = [part for part in re.split("([-()+*/])", function_details['function_formula']) if part]
                try:
                    general_function.save()
                    res = {
                      'result': 'ok',
                    }
                except:
                    res = {
                      'result': 'error',  
                    }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
            elif int(function_type) == 2:
                try:
                    continuity_function = ContinuityFunction.objects.get(id=function_details['id'])
                except:
                    continuity_function = ContinuityFunction()
                anly_head = AnalyticalHead.objects.get(id=function_details['select_head'])
                continuity_function.category = category
                continuity_function.function_name = function_details['function_name']
                continuity_function.description = function_details['function_description']
                continuity_function.function_type = 'continuity'
                continuity_function.analytical_head = anly_head
                continuity_function.number_of_periods = function_details['no_of_periods']
                continuity_function.minimum_value = function_details['minimum_value']
                continuity_function.period_1 = function_details['period_1']
                continuity_function.period_2 = function_details['period_2']
                continuity_function.period_3 = function_details['period_3']
                try:
                    continuity_function.save()
                    res = {
                      'result': 'ok',
                    }
                except:
                    res = {
                      'result': 'error',  
                    }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
            elif int(function_type) == 3:
                try:
                    consistency_function = ConsistencyFunction.objects.get(id=function_details['id'])
                except:
                    consistency_function = ConsistencyFunction()
                anly_head = AnalyticalHead.objects.get(id=function_details['select_head'])
                consistency_function.category = category
                consistency_function.function_name = function_details['function_name']
                consistency_function.description = function_details['function_description']
                consistency_function.function_type = 'consistency'
                consistency_function.analytical_head = anly_head
                consistency_function.number_of_periods = function_details['no_of_periods']
                consistency_function.mean = function_details['mean']
                consistency_function.period_1 = function_details['period_1']
                consistency_function.period_2 = function_details['period_2']
                try:
                    consistency_function.save()
                    res = {
                      'result': 'ok',
                    }
                except:
                    res = {
                      'result': 'error',  
                    }
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'function_settings.html', {})

class General(View):

    def get(self, request, *args, **kwargs):
        general = Function.objects.get(id=request.GET.get('id'))
        items = []
        items.append({
                'id':general.id,
                'name': general.function_name,
                'description': general.description,
                'head': general.analytical_head.id,
                'formula': general.formula,
                'category': general.category.id,
            })
        if request.is_ajax():
            response = simplejson.dumps({
               'item_list': items
            })
            return HttpResponse(response, status=200, mimetype='application/json')


class Continuity(View):

    def get(self, request, *args, **kwargs):
        continuity_function = ContinuityFunction.objects.get(id=request.GET.get('id'))
        items = []
        items.append({
                'id':continuity_function.id,
                'name': continuity_function.function_name,
                'description': continuity_function.description,
                'head': continuity_function.analytical_head.id,
                'no_of_periods': continuity_function.number_of_periods,
                'minimum_value': continuity_function.minimum_value,
                'period_1': continuity_function.period_1,
                'period_2': continuity_function.period_2,
                'period_3': continuity_function.period_3,
                'category': continuity_function.category.id,
            })
        if request.is_ajax():
            response = simplejson.dumps({
               'item_list': items
            })
            return HttpResponse(response, status=200, mimetype='application/json')


class Consistency(View):

    def get(self, request, *args, **kwargs):
        consistency_function = ConsistencyFunction.objects.get(id=request.GET.get('id'))
        items = []
        items.append({
                'id':consistency_function.id,
                'name': consistency_function.function_name,
                'description': consistency_function.description,
                'head': consistency_function.analytical_head.id,
                'no_of_periods': consistency_function.number_of_periods,
                'minimum_value': consistency_function.minimum_value,
                'period_1': consistency_function.period_1,
                'period_2': consistency_function.period_2,
                'mean': consistency_function.mean,
                'category': consistency_function.category.id,
            })
        if request.is_ajax():
            response = simplejson.dumps({
               'item_list': items
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