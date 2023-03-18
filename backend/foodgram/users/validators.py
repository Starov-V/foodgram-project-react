from re import match

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response


def validate_username(value):
    pattern = r'^[\w.@+-]+$'
    if match(pattern, value) is None:
        raise ValidationError(
            'Incorrect username',
            params={'value': value}
        )
    return value

def validate_password(value):
    if (len(value) < 8) :
        raise ValidationError(
            'Incorrect password: too short'
        )
    else:
        return value