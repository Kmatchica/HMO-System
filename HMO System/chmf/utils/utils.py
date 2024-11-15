from datetime import datetime
from django.db.models import Max
from access_app.models import access
from permission_app.models import permission
from modulelist_app.models import moduleslist
import sys
from django.apps import apps


def get_max_value(model, field_name):
    
    max_value = model.objects.aggregate(Max(field_name))
    return max_value[f"{field_name}__max"]

def generate_code(model, field_name, padding_width=5): 
    
    max_value = get_max_value(model, field_name)
    next_value = 1 if max_value is None else int(max_value) + 1
    formatted_code = f"{next_value:0{padding_width}d}"
    return formatted_code

def generate_policy_number(clientcode, membercode):    
    
    today = datetime.today()
    month_year = today.strftime("%m%y")    

    policy_number = f"{clientcode}-{month_year}-{membercode}"

    return policy_number

def get_app_config():
   
    frame = sys._getframe(1)  
    module_name = frame.f_globals.get('__name__')
    
    if not module_name:
        raise ValueError("Unable to determine the caller's module.")

    app_config = apps.get_containing_app_config(module_name)
    
    if not app_config:
        raise ValueError(f"No AppConfig found for module '{module_name}'.")
    
    return app_config

def has_permission(user, access_names, app_name):

    if user.is_authenticated:
        user_role_id = user.roleid.roleid
        permissions = permission.objects.filter(roleid=user_role_id)
        module_list = moduleslist.objects.filter(moduleappname=app_name)
        module_codes = [module.modulecode for module in module_list]
        permissions = permissions.filter(modulecode__in=module_codes)
        
        access_codes = access.objects.filter(
            accessname__in=access_names, 
            status='Active'
        ).values_list('accesscode', flat=True)
        
        permissions = permissions.filter(accesscode__in=access_codes)
        holder_values = [perm.holder for perm in permissions]
        
        return holder_values and holder_values[0] == 1

    return False
