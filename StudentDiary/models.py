from django.db import models
from django.utils import timezone
from Home.models import Student

# Create your models here.
class Diary(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='diaries')
    title = models.CharField(max_length=100)
    diary = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title  
    
    class Meta:
        verbose_name_plural = "Diaries"  