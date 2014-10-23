

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

from models import PublicUser, WatchList, CompareList
from web.models import Company
from web.utils import get_rating_details_by_star_count , get_rating_report

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
        return render(request, 'public_login.html', {
            'recaptcha_public_key': settings.RECAPTCHA_PUBLIC_KEY,
            'recaptcha_private_key': settings.RECAPTCHA_PRIVATE_KEY
        })

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
            try:
                public_user = PublicUser.objects.get(user=request.user)
                res = {'result': 'Ok'}
            except Exception as ex:
                logout(request)
                res = {'result': 'error'}
            if request.is_ajax():
                response = simplejson.dumps(res)
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

class StarRating(View):

    def get(self, request, *args, **kwargs):

        star_count = request.GET.get('star_count', '')
        if request.is_ajax() and star_count:
            response = get_rating_details_by_star_count(request, star_count)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'star_rating.html', {'star_count': star_count})

class StarRatingReport(View):

    def get(self, request, *args, **kwargs):

        isin_code = request.GET.get('isin_code', '')
        if request.is_ajax() and isin_code:
            response = get_rating_report(request, [isin_code])
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'star_rating_report.html', {'isin_code': isin_code})

class AddToWatchlist(View):

    def post(self, request, *args, **kwargs):

        isin_code = request.POST.get('isin_code', '')
        if request.is_ajax() and isin_code:
            company = Company.objects.get(isin_code=isin_code)
            try:
                public_user = PublicUser.objects.get(user=request.user)
                watch_list, created = WatchList.objects.get_or_create(user=public_user)
                if watch_list.companies.all().count() < 20:
                    watch_list.companies.add(company)
                    watch_list.save()
                    res = {
                        'result': 'ok',
                    }
                else:
                    res = {
                        'result': 'error_stock_exceed',
                        'error_message': 'You can add maximum 20 stocks in watch list'
                    }
            except Exception as ex:
                res = {
                    'result': 'error',
                    'message': str(ex),
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')


class AddToComparelist(View):

    def post(self, request, *args, **kwargs):

        isin_code = request.POST.get('isin_code', '')
        if request.is_ajax() and isin_code:
            company = Company.objects.get(isin_code=isin_code)
            try:
                public_user = PublicUser.objects.get(user=request.user)
                compare_list, created = CompareList.objects.get_or_create(user=public_user)
                if compare_list.companies.all().count() < 4:
                    compare_list.companies.add(company)
                    compare_list.save()
                    res = {
                        'result': 'ok',
                    }
                else:
                    res = {
                        'result': 'error_stock_exceed',
                        'error_message': 'You can add maximum 4 stocks in compare list'
                    }
            except:
                res = {
                    'result': 'error',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')

class ViewWatchList(View):

    def get(self, request, *args, **kwargs):
        ratings = []
        isin_code = request.GET.get('isin_code', '')
        if request.is_ajax and isin_code:
            public_user = PublicUser.objects.get(user=request.user)
            watch_lists = WatchList.objects.filter(user=public_user)
            compare_lists = CompareList.objects.filter(user=public_user)
            for watch_list in watch_lists:
                company = watch_list.company
                model_score = CompanyModelScore.objects.filter(company=company)
                if model_score.count() > 0:
                    model_score = model_score[0]
                    rating = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'isin_code': company.isin_code,
                        'industry': company.industry.industry_name,
                        'star_rating': "*" * int(model_score.star_rating) if model_score.star_rating else '',
                        'score': model_score.points,
                        'brief_comment': model_score.comment,
                        'company_in_watch_list': 'true' if company_in_watch_list else 'false',
                        'company_in_compare_list': 'true' if company_in_compare_list else 'false',
                        'added_on': watch_list.added_on.strftime('%d/%m/%Y'),
                        'rating_changed_date': model_score.updated_date.strftime('%d/%m/%Y'),
                    }
                else:
                    rating = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'star_rating': 'Data not available' if not company.is_all_data_available else 'No Rating available'
                    }
                ratings.append(rating)
            response = simplejson.dumps({
                'star_ratings': ratings,
                'watch_list_count': watch_lists.count(),
                'compare_list_count': compare_lists.count(),
            })
            return response
        return render(request, 'view_watch')


