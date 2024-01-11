"""
Database models.
"""
# import uuid
# import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# def recipe_image_file_path(instance, filename):
#     """Generate file path for new recipe image."""
#     ext = os.path.splitext(filename)[1]
#     filename = f'{uuid.uuid4()}{ext}'
#
#     return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        # creates a new instance of the user model
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # sets the hashed password for the user instance in the password field (base class = AbstractBaseUser). also None means you can pass it  later!
        # set_password is used for securely setting and hashing a users password before storing it.
        # check_password is used for securely comparing a raw password with the stored hashed password to verify if they match.
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        #  passing following args can be useful in scenarios where you have multiple databases and want to make sure that the manager and the model are consistently using the same database.
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    #  is_superuser with default = False is in PermissionsMixin
    objects = UserManager()

    USERNAME_FIELD = 'email'


# class Recipe(models.Model):
#     """Recipe object."""
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     time_minutes = models.IntegerField()
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     link = models.CharField(max_length=255, blank=True)
#     tags = models.ManyToManyField('Tag')
#     ingredients = models.ManyToManyField('Ingredient')
#     image = models.ImageField(null=True, upload_to=recipe_image_file_path)
#
#     def __str__(self):
#         return self.title
#
#
# class Tag(models.Model):
#     """Tag for filtering recipes."""
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#
#     def __str__(self):
#         return self.name
#
#
# class Ingredient(models.Model):
#     """Ingredient for recipes."""
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#
#     def __str__(self):
#         return self.name
