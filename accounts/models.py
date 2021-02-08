from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser 

# Create your models here. 

class UserProfileManager(BaseUserManager):
    def create_user(self, email, password=None):
        '''
        Creates and saves a User with the given email and password.
        '''
        if not email:
            raise ValueError('User must have an valid email address')

        user = self.model(
            email=email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        '''
        Creates and saves a SuperUser with the given email and password.
        '''
        user = self.create_user(
            email,
            password=password,
        )
       
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=100,
        unique=True,
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
       return self.is_superuser

    def has_module_perms(self, app_label):
       return self.is_superuser

class OTP(models.Model):
    otp = models.CharField(max_length=20)
    user = models.OneToOneField(UserProfile,related_name='otp',on_delete=models.CASCADE)
    is_password = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
