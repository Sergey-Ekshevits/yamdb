from django.core.exceptions import ValidationError


def username_not_me(val):
    if val.lower() == 'me':
        raise ValidationError('Имя пользователя не может быть \'me\'')