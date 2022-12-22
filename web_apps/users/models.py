from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user manager class
    """

    use_in_migrations = True

    def _create_user(
            self, email, password, full_name, **extra_fields):
        """
        Create and save a User with the given email and password
        :param email: Email of the User
        :param password: Password of the User
        :param full_name: Full Name of the User
        :param phone_number: Phone Number of the User
        :return: Return of object model User
        """

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email, password, full_name, **extra_fields):
        return self._create_user(
            email, password, full_name, **extra_fields
        )

    def create_superuser(
        self, email, password, full_name, **extra_fields
    ):
        """
        Create and save a User with superuser privilege
        """
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self._create_user(
            email, password, full_name, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """

    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True
    )
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
