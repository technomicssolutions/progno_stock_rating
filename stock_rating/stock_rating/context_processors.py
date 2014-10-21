from django.contrib.sites.models import Site
from django.db import models
from web.models import *
from public.models import PublicUser

def site_variables(request):
	user_permission = ''
	if request.user.is_authenticated():	
		if request.user.publicuser_set.all().count() == 0:	
			if request.user.is_superuser:				
				user_permission, created = UserPermission.objects.get_or_create(user=request.user, data_upload=True, field_settings=True, score_settings=True, function_settings=True, analytical_heads=True)	   		
		   	else:
		   		user_permission = UserPermission.objects.get(user = request.user)	   		
	return {
	 'user_permission': user_permission,
	}