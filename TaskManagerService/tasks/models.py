from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from TaskManagerService.tasks.managers import UserManager


class User(AbstractUser):
    ...


class Customer(User):
    ...


class Employer(User):
    ...


class Task(models.Model):
    ...
