from django.db import models
from Home.models import Student

# Create your models here.
class TestScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    score = models.IntegerField(null=True)

    def __str__(self): 
        return self.student.full_name