from datetime import datetime
from django import template
from django.db.models import Max
from access_app.models import access
from permission_app.models import permission
from modulelist_app.models import moduleslist
import sys
from django.apps import apps
import re
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .models import CodeCounter


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

def generate_approval_code(model, field_name, status, padding_width=6):
    
    prefix = "1C" if status == "Approved" else "1D"
    year_part = datetime.now().strftime("%y")
    maxValue = get_max_value(model, field_name)
    nextValue = 1 if maxValue is None else int(maxValue) + 1
    paddedApprovalCode = str(nextValue).zfill(padding_width)

    return f"{prefix}{year_part}-{paddedApprovalCode}"

def reset_counter(counter_obj):
    
    if counter_obj.counterresetbasis.lower() == "year":
        current_year = now().year
        if str(current_year) not in counter_obj.countername:
            counter_obj.counter = 0  # Reset  counter
            counter_obj.countername = str(current_year)  # Update  counter name to  current year
            counter_obj.save()
    return counter_obj

def increment_counter(status):
    
    current_year = now().year

    # Get or create  counter for  current year
    counter_obj, created = CodeCounter.objects.get_or_create(
        countername=str(current_year),
        defaults={"counterresetbasis": "Year"}
    )

    # Use  reset_counter utility
    counter_obj = reset_counter(counter_obj)

    # Increment  counter
    counter_obj.counter += 1
    counter_obj.save()

    # Format  code
    year_suffix = str(current_year)[-2:]  
    formatted_code = f"{status}{year_suffix}-{counter_obj.counter:06d}"

    return formatted_code

def validate_field(value, field_type, queryset=None, field_name=None):
        
    value = ' '.join(value.strip().split()) # trim spaces
    
    if field_type == 'duplicate' and queryset and field_name: # duplicate check
        if queryset.filter(**{field_name: value}).exists():
            raise ValidationError(f"{field_name.capitalize()} '{value}' already exists.")
    
    elif field_type == 'letters':
        if not all(c.isalpha() or c.isspace() for c in value): # letters only validation
            raise ValidationError("This field accepts letters and spaces only.")  
    
    elif field_type == 'numbers':# numbers only validation
        if not value.isdigit():
            raise ValidationError("This field accepts numbers only.")
    
    
    elif field_type == 'email':# Email Format Validation
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zAZ0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise ValidationError("Enter a valid email address.")
        
    elif field_type == 'allow_special_chars' and not re.match(r'^[a-zA-Z0-9\s!@#$%^&*(),.?":{}|<>]*$', value): # allow special characters
            raise ValidationError("This field contains invalid characters.")
    
    elif field_type == 'date_format':
        try:
            datetime.strptime(value, '%Y-%m-%d')  #validate date format
        except ValueError:
            raise ValidationError("Date must be in YYYY-MM-DD format.")
    
    return value
