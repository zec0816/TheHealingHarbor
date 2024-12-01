from django.db import models
from django.utils import timezone
from Home.models import Counselor

# Create your models here.
class Info(models.Model):
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='infos')
    title = models.CharField(max_length=100)
    info = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title  #return title of info section as a string
    
    class Meta:
        verbose_name_plural = "Infos"  #set the plural name of the model