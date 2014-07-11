import re

from django import template
register = template.Library()

from web.models import UserPermission

@register.filter        
def has_permission(value, user):
    print "user=====", user
    if user.is_superuser:
        return True
    else:
        permision = UserPermission.objects.get(user=user)
        if value == 'data_upload':
            return permision.data_upload
        elif value == 'score_settings':
            return permision.score_settings
        elif value == 'funcion_settings':
            return permision.funcion_settings
        elif value == 'field_settings':
            return permision.field_settings
        elif value == 'analytical_heads':
            return permision.analytical_heads
        else:
            return False

    
@register.filter
def uppercase(value):
	return value.upper()

@register.filter
def slugify_with_underscore(value):
    return re.sub(r"\s+", '_', value)

