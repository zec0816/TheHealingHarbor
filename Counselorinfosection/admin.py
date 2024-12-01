from django.contrib import admin
from .models import Info

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display="counselor","title","info" #display fields when viewing Info

admin.site.register(Info,MemberAdmin)