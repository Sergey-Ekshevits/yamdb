import random
import string

from django.core.mail import send_mail


def confirmation_code_generator():
    return str(''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(12)))


def send_verification_mail(email, code):
    subject = 'Код подтверждения для входа на YaMDB'
    message = f'Ваш код подтверждения для входа:\n{code}\n'
    from_email = 'webmaster@localhost'
    recipient_list = [email, ]
    send_mail(subject, message, from_email, recipient_list)
