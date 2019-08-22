from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# extends from user, already has username, email,first/last name


class UserProfileInfo(models.Model):

    # create relatinship (don't inherit from User)
    # if you want them to have other fields, use oneToone
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want,blank menas optional
    portfolio_site = models.URLField(blank=True)
    # pictures will be kept in media folder
    # work with images, need python Imaging lib: pip install pillow
    # or : pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username
