from django.core.mail import send_mail


def send_verification_mail(email, code):
    """Функция отправки e-mail с кодом доступа."""

    subject = 'Код подтверждения для входа на YaMDB'
    message = f'Ваш код подтверждения для входа:\n{code}\n'
    from_email = 'webmaster@localhost'
    recipient_list = [email, ]
    send_mail(subject, message, from_email, recipient_list)
