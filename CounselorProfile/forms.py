from django import forms
from django.contrib.auth.models import User
from Home.models import User, Counselor


class UpdateUserForm(forms.ModelForm):
    username = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    
    class Meta:
        model = User
        fields = ['username']


class UpdateCounselorForm(forms.ModelForm):
    counselor_profile = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    self_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    qualification = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Counselor
        fields = ['counselor_profile', 'full_name', 'phone_number', 'self_description', 'qualification']