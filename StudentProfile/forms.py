from django import forms
from django.contrib.auth.models import User
from Home.models import User, Student


class UpdateUserForm(forms.ModelForm):
    username = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    
    class Meta:
        model = User
        fields = ['username']


class UpdateStudentForm(forms.ModelForm):
    student_profile = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ['student_profile', 'full_name', 'phone_number']