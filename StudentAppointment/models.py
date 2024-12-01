from django.db import models
from Home.models import Student, Counselor
from CounselorSchedule.models import Timeslot
from django.utils import timezone

# Create your models here.

class Appointments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='studentappointment')
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='counselorappointment')
    timeslot = models.ForeignKey(Timeslot, on_delete=models.CASCADE, related_name='counselortimeslots')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def delete(self, *args, **kwargs):
      self.timeslot.is_booked = False
      self.timeslot.save()
      super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.student} booked for {self.timeslot.date}"
    
    class Meta:
        verbose_name_plural = "Student Appointments"
