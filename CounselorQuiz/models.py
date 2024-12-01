from django.db import models
from Home.models import Counselor

# Create your models here.
class QuizQuestion(models.Model):
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=200)

    def __str__(self): 
        return self.question_text
    
    class Meta:
        verbose_name_plural = "Quiz Questions"

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=200)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.option_text
    
    class Meta:
        verbose_name_plural = "Quiz Options"
    