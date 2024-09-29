# Import
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os
import random


# Functions
def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    min = 1000000000000
    max = 9999999999999

    while True:
        number = random.randint(min, max)
        with open("profile_image_numbers.txt", "a+") as file:
            file.seek(0)
            tf_list = []
            for line in file:
                if str(number)+"\n"==line:
                    tf_list.append(1)
                else:
                    tf_list.append(0)
            if 1 in tf_list:
                pass
            else:
                filename = str(number)+"."+ext
                file.write(str(number)+"\n")
                break
                

    return os.path.join('profile_images', str(instance.id), filename)


def post_image_path(instance, filename):
    ext = filename.split('.')[-1]
    min = 1000000000000
    max = 9999999999999

    while True:
        number = random.randint(min, max)
        with open("post_image_numbers.txt", "a+") as file:
            file.seek(0)
            tf_list = []
            for line in file:
                if str(number)+"\n"==line:
                    tf_list.append(1)
                else:
                    tf_list.append(0)
            if 1 in tf_list:
                pass
            else:
                filename = str(number)+"."+ext
                file.write(str(number)+"\n")
                break
                

    return os.path.join('post_image', str(instance.user.id), filename)


def story_image_path(instance, filename):
    ext = filename.split('.')[-1]
    min = 1000000000000
    max = 9999999999999

    while True:
        number = random.randint(min, max)
        with open("story_image_numbers.txt", "a+") as file:
            file.seek(0)
            tf_list = []
            for line in file:
                if str(number)+"\n"==line:
                    tf_list.append(1)
                else:
                    tf_list.append(0)
            if 1 in tf_list:
                pass
            else:
                filename = str(number)+"."+ext
                file.write(str(number)+"\n")
                break
                

    return os.path.join('story_image', str(instance.user.id), filename)

# Define the Story model
class Story(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=post_image_path)
    date_uploaded = models.DateTimeField(default=timezone.now)

# Define the Post model
class Post(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=post_image_path)
    caption = models.TextField(max_length=1000)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    date_uploaded = models.DateTimeField(default=timezone.now)

# Define the Following model
class Following(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, email, **extra_fields)

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'main_page_customuser'
    email = models.CharField(max_length=100, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    profile_image = models.ImageField(upload_to=profile_image_path, blank=True, null=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    numof_posts = models.IntegerField(default=0)
    numof_followers = models.IntegerField(default=0)
    numof_following = models.IntegerField(default=0)
    followers = models.TextField
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_private = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

# Messages model
class Messages(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reciever')
    message = models.TextField(max_length=1000)
    date_uploaded = models.DateTimeField(default=timezone.now)
