from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, Student, Counselor
from django.db import models

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['first_name', 'last_name']  # Exclude first_name and last_name fields

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_student', 'is_counselor', 'is_staff', 'is_superuser')}),
    )

    list_display = ('username', 'is_student', 'is_counselor', 'is_staff')
    list_filter = ["is_staff", "is_student", "is_counselor"]
    search_fields = ('username',)
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        # Save the user instance
        super().save_model(request, obj, form, change)

        # Check if the user is a student or counselor and create the corresponding instance
        if obj.is_student:
            student = Student.objects.create(user=obj)
            student.save()
        elif obj.is_counselor:
            counselor = Counselor.objects.create(user=obj)
            counselor.save()

class CustomStudentAdmin(admin.ModelAdmin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='student')
    list_display = ('user', 'full_name', 'phone_number')
    ordering = ('created_at',)
    list_filter = ('created_at',)

    def delete(self, *args, **kwargs):
        # Delete the associated User instance
        self.user.delete()
        super().delete(*args, **kwargs)


class CustomCounselorAdmin(admin.ModelAdmin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='counselor')
    list_display = ('user', 'full_name', 'phone_number')
    ordering = ('created_at',)
    list_filter = ('created_at',)

    def delete(self, *args, **kwargs):
        # Delete the associated User instance
        self.user.delete()
        super().delete(*args, **kwargs)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, CustomStudentAdmin)
admin.site.register(Counselor, CustomCounselorAdmin)
