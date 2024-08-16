from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,username,email, password=None, company=None, terms_and_condition=False, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, company=company, terms_and_condition=terms_and_condition, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, company=None, terms_and_condition=False, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username, email, password, company, terms_and_condition, **extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.CharField(unique=True)
    company = models.CharField(max_length=100)
    terms_and_condition = models.BooleanField()
    role = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','company','terms_and_condition']

    def __str__(self):
        return self.username

class TeacherDetails(models.Model):
    teacher_id = models.CharField(max_length=100)
    teacher_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    pan_card = models.CharField(max_length=100)
    aadhar_card = models.CharField(max_length=100)
    mobile_number =  models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    salary =  models.CharField(max_length=100)
    alter_number =  models.CharField(max_length=100)
    date_of_birth = models.DateField()
    previous_school_name = models.CharField(max_length=250)
    transport_fees =  models.CharField(max_length=100)
    graduation_complete = models.BooleanField(default=False)
    bed_complete = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            last_instance = TeacherDetails.objects.order_by('-teacher_id').first()
            if last_instance:
                last_sequence = int(last_instance.teacher_id[2:])
                next_sequence = last_sequence + 1
                self.teacher_id = f"TR{str(next_sequence).zfill(4)}"
            else:
                self.teacher_id = "TR0001"
        super().save(*args, **kwargs)