from django.core.exceptions import ValidationError
from datetime import datetime

numbers = ('1','2','3','4','5','6','7','8','9','0')

def validate_yearfilms(value):
    print("Execute the method \"validate_yearfilms\"")
    value = int(value)
    if value <= datetime.today().year:
        return value
    else:
        raise ValidationError("The year is invalid")

def validate_studioname(value):
    print("Execute the method \"validate_studioname\"")
    for i in numbers:
        if i in value:
            raise ValidationError("The studio can't have numeric characters")
        else:
            continue
    return value
