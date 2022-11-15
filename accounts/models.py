from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


def _get_profile_image_filepath(self):
    return f'images/user_images/{self.pk}/profile_image.png'

def _get_default_profile_image():
    return 'images/default_profile_image.jpg'
    

class User(AbstractBaseUser):
    email = models.EmailField(_("email address"), max_length=260, unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    profile_image = models.ImageField(_("profile image"), upload_to=_get_profile_image_filepath, null=True, blank=True, default=_get_default_profile_image)
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), auto_now=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_admin = models.BooleanField(_("admin status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)
    is_email_verified = models.BooleanField(_("email verification status"), default=False)
        
    objects = UserManager()
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True