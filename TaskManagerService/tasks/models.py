from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class ROLES:
    EMPLOYER = 'employer'
    ADMIN = 'admin'
    CUSTOMER = 'customer'
    roles = (EMPLOYER, ADMIN, CUSTOMER)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: "
                                         "'+999999999'. Up to 15 digits allowed.")

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    surname = models.CharField(_("surname"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"User({self.id}, {self.email}, {self.phone_number if self.phone_number else None})"

    class Meta:
        abstract = True


class User(AbstractUser):
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_full_name(self):
        full_name = "%s %s %s" % (self.first_name, self.last_name, self.surname)
        return full_name.strip()

    def roles(self):
        return self.groups.all()

    def check_role(self, role):
        return self.groups.filter(name=role).exists()


class Task(models.Model):
    STATUS_ACTIVE = "IP"
    STATUS_WAITING = "WE"
    STATUS_DONE = "DN"

    STATUS_CHOICES = {
        STATUS_ACTIVE: 'In process',
        STATUS_WAITING: 'Waiting for employer',
        STATUS_DONE: 'Done',
    }
    task_goal = models.CharField(max_length=350)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_WAITING)
    report = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_closed = models.DateTimeField(default=None, null=True)
    employer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='employer_tasks', null=True)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='customer_tasks', null=True)

    def __str__(self):
        return f"Task({self.status}, {self.employer}, {self.date_created})"

    def is_working(self):
        return self.status == self.STATUS_ACTIVE

    def is_active(self):
        return self.status == self.STATUS_WAITING

    def is_done(self):
        return self.status == self.STATUS_DONE

    def save(self, *args, **kwargs):
        if self.customer is None:
            raise ValueError("Cannot save task without customer")
        if self.date_closed is not None and self.report is None:
            raise ValueError("Cannot close task without report")
        super(Task, self).save(*args, **kwargs)
