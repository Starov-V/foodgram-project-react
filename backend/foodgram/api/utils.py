import random
import string

from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def send_code(email):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(8))
    send_mail(
        'Confirmation code',
        f'Confirmation code: {code}',
        from_email=settings.FROM_EMAIL,
        recipient_list=[email],
    )
    return code


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    tokens = {
        'token': str(refresh.access_token),
    }
    return tokens
