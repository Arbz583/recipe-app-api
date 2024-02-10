"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
# the convention of including the instance argument in file path functions in Django is reasonable because it allows you to access attributes and fields of the model instance if needed when constructing the file path. it is not optional though!
# With a custom file path function, you have the flexibility to define the storage path and filename based on specific requirements. This allows for a more customized and tailored approach to organizing files.
# Unique paths add a level of security by making it more difficult for unauthorized users to guess file locations.
def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    # for getting file extension filename.split('.')[1] does not work correctly with filename with multiple dots but following does!
    ext = os.path.splitext(filename)[1]
    # it is almost impossible that two uuid be same because its algorithm  providing a large space of possible values (2^122)
    filename = f'{uuid.uuid4()}{ext}'

    # we do not use hardcoding so Cross-Platform Compatibility(/ or \), also handle avoiding double seperator(//=/)
    return os.path.join('uploads', 'recipe', filename)


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


class Recipe(models.Model):
    """Recipe object."""
    # if you do not pass string (get_user_mode for example), that means user must be loaded first and we can not gaurantee that!
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(_('title'), max_length=255)
    # empty is allowed and if you do not send it set empty string "" in database.
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    # maximum of 5 digits in total, with up to 2 digits after the decimal point like 123.45.
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    # null is allowed and if you do not send it set null in database.
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
