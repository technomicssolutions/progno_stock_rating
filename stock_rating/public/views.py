

import simplejson
import ast
import urllib

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings

from models import PublicUser
from web.utils import get_rating_details_by_star_count , get_rating_report



class Home(View):
    def get(self, request, *args, **kwargs):
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
            print "user is active"
            login(request, user)
            try:
                public_user = PublicUser.objects.get(user=request.user)
                res = {'result': 'Ok'}
                print "public user"
            except Exception as ex:
                logout(request)
                res = {'result': 'error'}
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
        return render(request, 'administration.html', {})

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('public_login'))

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
