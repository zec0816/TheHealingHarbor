from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image

from django.core.validators import FileExtensionValidator
# Create your models here.

class User(AbstractUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    username = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_counselor = models.BooleanField(default=False)

class Student(models.Model):          #when student instance is deleted , user instance will also be deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    
    student_profile = models.ImageField(default="default.png", upload_to="student_profiles", validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])])
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
     return self.user.username    #return the username in form of string
    
    def save(self, *args, **kwargs):
      super().save(*args, **kwargs)
      
      img = Image.open(self.student_profile.path)   #Open the student profile image using PIL library
      if img.height > 400 or img.width > 400:
        new_img = (400, 400)          #Resize the image if its height or width exceeds 400 px
        img.thumbnail(new_img)
        img.save(self.student_profile.path)     #save the image back to the original path

    def delete(self, *args, **kwargs):
        # Delete the associated User instance
        self.user.delete()
        super().delete(*args, **kwargs)

class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='counselor')
    
    counselor_profile = models.ImageField(default="default.png", upload_to="counselor_profiles", validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])])
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    self_description = models.TextField(max_length=300)
    qualification = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
     return self.user.username
    
    def save(self, *args, **kwargs):
      super().save(*args, **kwargs)
      
      img = Image.open(self.counselor_profile.path)
      if img.height > 400 or img.width > 400:
        new_img = (400, 400)
        img.thumbnail(new_img)
        img.save(self.counselor_profile.path)

    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)
