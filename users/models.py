from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from .managers import UserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    mobile_phone = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^(?:\+20|0)?1[0125]\d{8}$',
                message="Phone number must be entered in the format: '+201001234567', '01001234567', etc."
            ),
        ]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_phone']

    objects = UserManager()

    def __str__(self):
        return self.email