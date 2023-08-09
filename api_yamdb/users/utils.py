import random
from django.core.mail import send_mail

# from rest_framework_simplejwt.tokens import AccessToken
#
#
# def get_token_for_user(user):
#     refresh = AccessToken.for_user(user)
#
#     return {
#         'token': str(refresh.access_token),
#     }


def confirmation_code_generator():
    return int(''.join([str(random.randint(0,10)) for _ in range(6)]))


def send_verification_mail(email, code):
    generated_code = confirmation_code_generator()
    subject = 'Код подтверждения'
    message = f'Ваш код подтверждения для входа:\n{code}\n'
    from_email = 'webmaster@localhost'
    recipient_list = [email, ]
    send_mail(subject, message, from_email, recipient_list)