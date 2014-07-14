
import simplejson
import ast

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from models import UserPermission, DataField, FunctionCategory, AnalyticalHead

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
        item_list = FunctionCategory.objects.all()
        an_heads = AnalyticalHead.objects.all()
        context = {'item_list': item_list, 'an_heads': an_heads}
        return render(request, 'function_settings.html', context)


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


class SaveUser(View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            user_details = ast.literal_eval(request.POST['user_details'])
            print request.POST['user_details']
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