

import simplejson
import ast
import lxml.etree as ET
import numpy as np 

from collections import OrderedDict
from math import sqrt

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

from models import PublicUser

def rpHash(person): 
    hash = 5381 
  
    value = person.upper() 
    for caracter in value: 
        hash = (( np.left_shift(hash, 5) + hash) + ord(caracter)) 
    hash = np.int32(hash) 

class Home(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'home.html', {})

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'public_login.html', {})

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
            if request.is_ajax():
                response = simplejson.dumps({'result': 'Ok'})
                return HttpResponse(response, status=200, mimetype='application/json')
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'login.html', context)     

class Signup(View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            user_details = ast.literal_eval(request.POST['user_details'])
            user = User()
            user.username = user_details['username']
            user.first_name = user_details['fullname']
            if user_details['password']:
                user.set_password(user_details['password'])
            try:
                user.save()   
                public_user = PublicUser()
                public_user.user = user
                public_user.save()
                res = {
                    'result': 'ok',
                }
            except:
                res = {
                    'result': 'error',
                }
            user = authenticate(username=user.username, password=user_details['password'])
            if user and user.is_active:
                login(request, user)
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'administration.html', {})

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('public_login'))


# import numpy as np 
# ------------------------------ 
# def rpHash(person): 
#     hash = 5381 
  
#     value = person.upper() 
#     for caracter in value: 
#         hash = (( np.left_shift(hash, 5) + hash) + ord(caracter)) 
#     hash = np.int32(hash) 
# ----------------------------- 
  
# if rpHash(request.form['realPerson']) == request.form['realPersonHash']: 
#     # Accepted 
# else: 
#     # Rejected