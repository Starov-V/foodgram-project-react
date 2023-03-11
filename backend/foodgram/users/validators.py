from re import match

from django.core.exceptions import ValidationError


def validate_username(value):
    pattern = r'^[\w.@+-]+$'
    if match(pattern, value) is None:
        raise ValidationError(
            'Incorrect username',
            params={'value': value}
        )
    return value