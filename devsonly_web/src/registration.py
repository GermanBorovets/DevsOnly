from datetime import date

from django.core.exceptions import ValidationError
from main.models import User


def validate_letters(field: str) -> None:
    # Validates if form field contains only letters
    if not all(char.isalpha() for char in field):
        raise ValidationError('Field must contain only letters.',
                              code='invalid')


def validate_username(username) -> None:
    if all(char.isdigit() for char in username):
        raise ValidationError('Username must not consist only of digits.',
                              code='invalid username')
    if User.objects.filter(username=username).exists():
        raise ValidationError('This username is already used.',
                              code='used username')


def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError('This email is already used.',
                              code='used email')


def validate_password(password) -> None:
    min_length = 8
    if len(password) < min_length:
        raise ValidationError('Password must be at least %(min_length)s symbols long.',
                              params={'min_length': min_length},
                              code='weak')
    if not any(char.isalpha() for char in password):
        raise ValidationError('Password must contain at least 1 letter.',
                              code='weak')
    if not any(char.isupper() for char in password):
        raise ValidationError('Password must contain at least 1 capital letter.',
                              code='weak')
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least 1 digit.',
                              code='weak')


def validate_birth_date(birth_date: date) -> None:
    if birth_date > date.today() or birth_date < date(1900, 1, 1):
        raise ValidationError('Date of birth is inauthentic.',
                              code='invalid date')


def validate_pronouns(pros: str) -> None:
    if  pros.find('/') == -1 or pros.find('/') != pros.rfind('/'):
        raise ValidationError('Format must be: "they/them".',
                              code='invalid pros')
    for char in pros:
        if char != '/' and not char.isalpha():
            raise ValidationError('Format must be: "they/them".',
                                  code='invalid pros')
