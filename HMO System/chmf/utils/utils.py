from datetime import datetime
from django.db.models import Max

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

