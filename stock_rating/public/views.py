

import simplejson
import ast
import urllib
import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

from models import PublicUser, WatchList, CompareList
from web.models import Company, CompanyModelScore
from web.utils import get_rating_details_by_star_count , get_rating_report


def public_login_required(function, login_url):
    def wrapper(request, *args, **kw):
        user = request.user  
        if user.is_authenticated:
            if not is_public_user(request):
                return HttpResponseRedirect(login_url)
            else:
                return function(request, *args, **kw)
        else:
            return HttpResponseRedirect(login_url)        
    return wrapper



def is_public_user(request):
    try:
        public_user = PublicUser.objects.get(user=request.user)
        return True
    except Exception:
        return False

class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            if  is_public_user(request):
                return render(request, 'home.html', {})
            else:
                return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('public_login'))

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
            if not is_public_user(request):
                logout(request)
                res = {'result': 'error'}
            else: 
                res = { 'result': 'Ok'}
            if request.is_ajax():
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
            return HttpResponseRedirect(reverse('home'))
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            if request.is_ajax():
                response = simplejson.dumps(context)
                return HttpResponse(response, status=200, mimetype='application/json')
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
        return render(request, 'home.html', {})

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('public_login'))

class StarRating(View):

    def get(self, request, *args, **kwargs):
        print "ajax", request.is_ajax()

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

class VerifyRecaptcha(View):
    def post(self, request, *args, **kwargs):
        url = "http://www.google.com/recaptcha/api/verify"
        data = urllib.urlencode({
            'privatekey': settings.RECAPTCHA_PRIVATE_KEY,
            'remoteip': request.POST['remoteip'],
            'challenge': request.POST['challenge'],
            'response': request.POST['response']
        })
        try:
            result = urllib.urlopen(url, data)
            result = result.readline().strip()
        except urllib.URLError, e:
            print e
            result = ''
        response = simplejson.dumps({'result': result})
        return HttpResponse(response, status=200, mimetype='application/json')

class AddToWatchlist(View):

    def post(self, request, *args, **kwargs):
        if not is_public_user(request):
            return HttpResponseRedirect(reverse('login'))
        isin_code = request.POST.get('isin_code', '')
        if request.is_ajax() and isin_code:
            company = Company.objects.get(isin_code=isin_code)
            try:
                public_user = PublicUser.objects.get(user=request.user)
                watch_list_companies = WatchList.objects.filter(user=public_user)
                if watch_list_companies.count() < 20:
                    watch_list, created = WatchList.objects.get_or_create(user=public_user, company=company)
                    current_date = datetime.datetime.now().date()
                    watch_list.added_on = current_date
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
                compare_list_companies = CompareList.objects.filter(user=public_user)
                if compare_list_companies.count() < 4:
                    compare_list, created = CompareList.objects.get_or_create(user=public_user, company=company)
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
        
        watch_lists_details = []
        if request.is_ajax():
            public_user = PublicUser.objects.get(user=request.user)
            watch_lists = WatchList.objects.filter(user=public_user)
            compare_lists = CompareList.objects.filter(user=public_user)
            for watch_list in watch_lists:
                company = watch_list.company
                model_score = CompanyModelScore.objects.filter(company=company)
                if model_score.count() > 0:
                    model_score = model_score[0]
                    compare_list = CompareList.objects.filter(user=public_user, company=company)
                    if compare_list.count() > 0:
                        company_in_compare_list = True
                    else:
                        company_in_compare_list = False
                    rating = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'isin_code': company.isin_code,
                        'industry': company.industry.industry_name,
                        'star_rating': "*" * int(model_score.star_rating) if model_score.star_rating else '',
                        'score': model_score.points,
                        'brief_comment': model_score.comment,
                        'company_in_compare_list': 'true' if company_in_compare_list else 'false',
                        'added_on': watch_list.added_on.strftime('%d/%m/%Y'),
                        'rating_changed_date': model_score.updated_date.strftime('%d/%m/%Y'),
                    }
                else:
                    rating = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'star_rating': 'Data not available' if not company.is_all_data_available else 'No Rating available'
                    }
                watch_lists_details.append(rating)
            response = simplejson.dumps({
                'watch_lists': watch_lists_details,
                'watch_list_count': watch_lists.count(),
                'compare_list_count': compare_lists.count(),
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'view_watch_list.html', {})

class ViewCompareList(View):

    def get(self, request, *args, **kwargs):
        compare_list_details = []
        # if request.is_ajax():

        return render(request, 'view_compare_list.html', {})



