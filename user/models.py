from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

role_choices = (
    ('System Admin', 'System Admin'),
    ('Executive Committee of the National Economic Council', 'Executive Committee of the National Economic Council'),
    ('Ministry of Planning', 'Ministry of Planning'),
    ('Executing Agency', 'Executing Agency'),

)

#   "End Choice Fields"


class UserManager(BaseUserManager):

    """Abstracting BaseUserManager for creating custom user system and
        custom login/superuser creating system."""

    def create_user(self, name, email, password=None):
        if not name:
            raise ValueError('Name is required')
        if not email:
            raise ValueError('Email is required')
        user = self.model(
            name=name,
            email=self.normalize_email(email),

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password=None):
        user = self.create_user(
            name=name,
            email=self.normalize_email(email),

            password=password
        )
        user.is_SYSADMIN = True
        user.is_ECNEC = True
        user.is_MOP = True
        user.is_EXEC = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    """Abstracting BaseUser model to add custom fields to user model for System Quest."""

    name = models.CharField(verbose_name='Name', max_length=22)
    email = models.EmailField(verbose_name='Email Address', max_length=50, unique=True)

    # student data

    user_role = models.CharField(verbose_name='User Role', max_length=100, choices=role_choices, null=True)

    # permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # staff permissions
    is_SYSADMIN = models.BooleanField(default=False)
    is_ECNEC = models.BooleanField(default=False)
    is_MOP = models.BooleanField(default=False)
    is_EXEC = models.BooleanField(default=False)
    is_appuser = models.BooleanField(default=False)

    # role_description = models.CharField(verbose_name='User Role', max_length=100, choices=role_description, null=True)
    # for teacher only

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    objects = UserManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

