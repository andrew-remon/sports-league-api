# third-party
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create my custom user manager for CustomUser model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, first name, last name and password.
        """

        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, first name, last name and password.
        """
        superuser = self.create_user(
            email,
            first_name,
            last_name,
            password,
        )

        superuser.is_admin = True
        superuser.save(using=self._db)
        return superuser


# Create my custom user model
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="email address",
        unique=True,
        max_length=255,
    )
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# note: I created a user with curl: email: dodo.remo2005@gmail.com, password: andrew_2005
