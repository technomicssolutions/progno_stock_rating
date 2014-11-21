

import simplejson
import ast
import urllib
import datetime
import urllib2
import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail


from models import PublicUser, WatchList, CompareList, Help
from web.models import  ( Company, CompanyModelScore, CompanyFunctionScore, NSEBSEPrice, \
    CompanyModelFunctionPoint, ParameterLimit)
from web.utils import get_rating_details_by_star_count , get_rating_report, get_company_details


def public_login_required(function, login_url):
    def wrapper(request, *args, **kw):
        request.session['next_url'] = request.get_full_path()
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
        user = request.user
        if request.user.is_authenticated():
            if  is_public_user(request):   
                if user.social_auth.all().count() > 0:
                    public_user, created = PublicUser.objects.get_or_create(user=user)
                    url = """http://graph.facebook.com/{0}/""".format(user.username)
                    p =  urllib2.urlopen(url)
                    p = p.readline()
                    p = ast.literal_eval(p)
                    public_user.fb_details = p
                    public_user.save()                             
                return render(request, 'home.html', {})
            else:
                return HttpResponseRedirect(reverse('dashboard'))
        else:
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
            if request.session.get('next_url', ''):
                next_url = request.session.get('next_url', '')
            else:
                next_url = '/'
            login(request, user)
            if not is_public_user(request):
                logout(request)
                res = {'result': 'error'}
            else: 
                res = { 'result': 'Ok', 'next_url': next_url}
            if request.is_ajax():
                response = simplejson.dumps(res)
                return HttpResponse(response, status=200, mimetype='application/json')
            
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(reverse('home'))
        else:
            result = {
                'message' : 'Username or password is incorrect'
            }
            if request.is_ajax():
                response = simplejson.dumps(result)
                return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'login.html', result)     

class ActivateAccount(View):
    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['user_id'])
            user.is_active = True
            user.save()
        except Exception as e:
            print str(e)
            pass
        return HttpResponseRedirect(reverse('public_login'))

class Signup(View):

    def post(self, request, *args, **kwargs):
        if request.session.get('next_url', ''):
            next_url = request.session.get('next_url', '')
        else:
            next_url = '/'
        if request.is_ajax():
            user_details = ast.literal_eval(request.POST['user_details'])
            user = User()
            user.username = user_details['username']
            user.first_name = user_details['fullname']
            user.email = user_details['username']
            if user_details['password']:
                user.set_password(user_details['password'])
            try:
                user.save()   
                user.is_active = False
                user.save()
                public_user = PublicUser()
                public_user.user = user
                public_user.save()
                email_to = user.email
                subject = " Progno Account Activation "
                message = " Please activate your account by clicking the following link " + settings.SITE_ROOT + "activate/"+str(user.id)+"/"
                from_email = settings.DEFAULT_FROM_EMAIL         
                send_mail(subject, message, from_email,[email_to])
                res = {
                    'result': 'ok',
                    'next_url': next_url,
                    'message': 'Account Activation link is sent to you email'
                }
            except:
                res = {
                    'result': 'error',
                }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'home.html', {})

class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('public_login'))

class StarRating(View):

    def get(self, request, *args, **kwargs):
        star_count = request.GET.get('star_count', '')
        order_by = request.GET.get('order_by', '')
        start = request.GET.get('start', '')
        end = request.GET.get('end', '')
        if request.is_ajax() and star_count:
            response = get_rating_details_by_star_count(request, star_count, order_by, start, end)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'star_rating.html', {'star_count': star_count})

class StarRatingReport(View):

    def get(self, request, *args, **kwargs):

        isin_code = request.GET.get('isin_code', '')
        company = Company.objects.get(isin_code=isin_code)
        if request.is_ajax() and isin_code:
            response = get_rating_report(request, [isin_code])
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'star_rating_report.html', {'company': company, 'isin_code': isin_code})

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
                    rating = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'isin_code': company.isin_code,
                        'industry': company.industry.industry_name,
                        'star_rating': int(model_score.star_rating.star_count) if model_score.star_rating else 0,
                        'score': model_score.points,
                        'brief_comment': model_score.star_rating.comment if model_score.star_rating else '',
                        'company_in_compare_list': 'true' if company_in_compare_list else 'false',
                        'added_on': watch_list.added_on.strftime('%d/%m/%Y') if watch_list.added_on else '',
                        'rating_changed_date': model_score.updated_date.strftime('%d/%m/%Y') if model_score.updated_date else '',
                        'change': int(model_score.star_rating_change) if model_score.star_rating_change else 0 ,
                        'pricing': pricing
                    }
                else:
                    rating = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'star_rating': 'Data not available' if not company.is_all_data_available else 'No Rating available'
                    }
                watch_lists_details.append(rating)
            response = simplejson.dumps({
                'watch_list': watch_lists_details,
                'watch_list_count': watch_lists.count(),
                'compare_list_count': compare_lists.count(),
            })
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'view_watch_list.html', {})

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
                    compare_list = CompareList.objects.filter(user=public_user)
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

class ChangeCompareList(View):

    def post(self, request, *args, **kwargs):
        new_stock = request.POST.get('new_stock_isin_code', '')
        current_stock = request.POST.get('current_stock_isin_code', '')
        public_user = PublicUser.objects.get(user=request.user)
        current_stock = Company.objects.get(isin_code=current_stock)
        current_stock_in_compare_list = CompareList.objects.filter(user=public_user, company=current_stock)
        current_stock_in_compare_list.delete();
        new_stock = Company.objects.get(isin_code=new_stock)
        compare_list, created = CompareList.objects.get_or_create(user=public_user, company=new_stock)
        compare_list.save()
        if request.is_ajax():
            res = {
                'result': 'ok',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        else:
            return HttpResponseRedirect(reverse('compare_list'))

class ViewCompareList(View):

    def get(self, request, *args, **kwargs):
        compare_lists_details = []
        if request.is_ajax():
            public_user = PublicUser.objects.get(user=request.user)
            compare_list = CompareList.objects.filter(user=public_user)
            i = 0
            an_heads = []
            for obj in compare_list:
                company = obj.company
                model_score = CompanyModelScore.objects.filter(company=company)
                if model_score.count() > 0: 
                    company_dict = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'isin_code': company.isin_code,
                        'industry': company.industry.industry_name,
                        'star_rating': int(model_score[0].star_rating.star_count) if model_score[0].star_rating else 0,
                        'model_score': model_score[0].points
                    }
                    model = model_score[0].analysis_model
                    analytical_heads = []
                    for analytical_head in model.analytical_heads.all():
                        if i==0:
                            head = {
                                'head_name': analytical_head.title,
                                'functions': []
                            }
                        functions_details = []
                        for function in analytical_head.function_set.all().order_by('order'):
                            try:                                                     
                                parameter = ParameterLimit.objects.get(analysis_model=model, function=function)
                                if i==0:
                                    head['functions'].append(function.function_name)   
                                function_score = CompanyFunctionScore.objects.filter(function=parameter.function, company=company)
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
                                if score is not None:
                                    functions_details.append({
                                        'funtion_name': function.function_name,
                                        'score': score
                                    })
                            except:
                                pass
                        analytical_heads.append({
                            'head_name': analytical_head.title,
                            'functions': functions_details,
                        })
                        if i == 0:
                            an_heads.append(head)
                    i = i+ 1
                    company_dict['analytical_heads'] = analytical_heads
                else:
                    company_dict = {
                        'company_name': company.company_name + ' - ' + company.isin_code,
                        'star_rating': 'Data not available' if not company.is_all_data_available else 'No Rating available'
                    }
                compare_lists_details.append(company_dict)
            response = simplejson.dumps({
                'compare_list': compare_lists_details,
                'analytical_heads': an_heads
            })
            return HttpResponse(response, status=200, mimetype='application/json')

        return render(request, 'view_compare_list.html', {})

class DeleteFromCompareList(View):
    def get(self, request, *args, **kwargs):
        isin_code = request.GET.get('isin_code', '')
        company = Company.objects.get(isin_code=isin_code)
        public_user = PublicUser.objects.get(user=request.user)
        compare_list_company = CompareList.objects.get(user=public_user, company=company)
        compare_list_company.delete()
        if request.is_ajax() and isin_code:
            res = {
                'result': 'ok',
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=200, mimetype='application/json')
        else:
            return HttpResponseRedirect(reverse('compare_list'))

class SearchCompany(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            response = get_company_details(request)
            return HttpResponse(response, status=200, mimetype='application/json')

class SearchResult(View):

    def get(self, request, *args, **kwargs):
        isin_code = request.GET.get('isin_code', '')
        company_name = ''
        if isin_code:
            company = Company.objects.get(isin_code=isin_code)
            company_name = company.company_name
        if request.is_ajax() and isin_code:
            response = get_rating_report(request, [isin_code])
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'search_result.html', {'isin_code': isin_code, 'company_name': company_name})

class HelpView(View):

    def post(self, request, *args, **kwargs):
        help = ast.literal_eval(request.POST['help'])
        help_obj = Help()
        help_obj.name =  help['name']
        help_obj.email = help['email']
        help_obj.message =  help['message']
        help_obj.save()
        email_to = User.objects.filter(is_superuser=True)[0].email
        subject = " Help Request From Stoklab "
        message = help['message']
        from_email = settings.DEFAULT_FROM_EMAIL         
        send_mail(subject, message, from_email,[email_to])
        if request.is_ajax():
            response = {
                'result': 'OK'
            }
            response = simplejson.dumps(response)
            return HttpResponse(response, status=200, mimetype='application/json')
        return render(request, 'home.html', {})




