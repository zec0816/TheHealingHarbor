from django.contrib import admin
from .models import Timeslot

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display="counselor","date","day","start","end"

admin.site.register(Timeslot,MemberAdmin)