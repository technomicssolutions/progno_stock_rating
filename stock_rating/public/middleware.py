
from social_auth.middleware import SocialAuthExceptionMiddleware
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from social_auth import exceptions as social_exceptions 
from social_auth.exceptions import AuthAlreadyAssociated  

class MySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if hasattr(social_exceptions, exception.__class__.__name__):
            if type(exception) == AuthAlreadyAssociated:
                return HttpResponseRedirect(reverse('dashboard'))

            return HttpResponse("catched: %s" % exception)
        else:
            raise exception