from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import ADMIN_EMAIL


def send_code(user):
    """Функция отправки кода подтверждения  на email."""
    subject = 'Код авторизации YaMDb'
    confirmation_code = default_token_generator.make_token(user)
    message = f'Код для авторизации на платформе YaMDb {confirmation_code} '
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    return send_mail(subject, message, admin_email, user_email)
