from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True, blank=False)
    password = models.CharField(max_length=20)
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS= ["username", "password"]
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    

class UserFollows(models.Model):
    # Your UserFollows model definition goes here
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
    user = models.ForeignKey("CustomUser", related_name="following", on_delete=models.CASCADE)
    followed_user = models.ForeignKey("CustomUser", related_name="followers", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'followed_user', )
    def __str__(self):
        return f"{self.user} suit {self.followed_user}"