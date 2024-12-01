from django.db import models
from datetime import datetime
from Home.models import Counselor
from django.core.exceptions import ValidationError

class Timeslot(models.Model):
    counselor = models.ForeignKey(Counselor, on_delete=models.CASCADE, related_name='schedule')
    date = models.DateField(null=True)
    start = models.TimeField(null=True)
    end = models.TimeField(null=True)
    day = models.CharField(max_length=100, null=True, editable=False)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.start} - {self.end}"

    def save(self, *args, **kwargs):
        if self.start > self.end:                  #validate the start time and end time
            raise ValidationError('Start time should be earlier than end time')

        if self.date:
            self.day = datetime.strftime(self.date, "%A")    #return the day of the week

        existing_timeslot = Timeslot.objects.filter(
            date=self.date,
            start=self.start,          #check whether the timeslot already exists 
            end=self.end
        ).exclude(pk=self.pk)  #ensures that the current Timeslot object is not considered a duplicate

        if existing_timeslot.exists():
            raise ValidationError('A timeslot with the same date and time already exists.')

        super().save(*args, **kwargs)

    def is_available(self):
        return not self.is_booked   #check whether the timeslot is available or not based on the value of the is_booked field
    
    class Meta:
        verbose_name_plural = "Counselor Schedules"