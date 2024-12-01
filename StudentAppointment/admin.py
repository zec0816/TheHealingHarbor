from django.contrib import admin
from .models import Appointments
from CounselorSchedule.models import Timeslot
# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'counselor', 'timeslot', 'timeslot__date')

    def timeslot__date(self, obj):
        return obj.timeslot.date

admin.site.register(Appointments, AppointmentAdmin)