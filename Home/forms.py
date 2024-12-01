from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django import forms
from .models import User
from django.core.validators import MinLengthValidator, RegexValidator

class RegistrationForm(UserCreationForm):
    username = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control',}))
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password',}))
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password',}))

    full_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control',}))
    phone_number = forms.CharField(
        max_length=100,
        required=True,
        validators=[
            MinLengthValidator(9, message="Phone number must be at least 9 digits long."),
            RegexValidator(r'^[0-9]+$', message="Phone number should only contain numbers."),
        ],
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}),
    )    
    role_choices = (
        ('counselor', 'Counselor'),
        ('student', 'Student'),
    )
    role = forms.ChoiceField(choices=role_choices, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2', 'full_name', 'phone_number', 'role')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False) #tells the method not to commit the changes immediately. Performing additional operations before saving

        role = self.cleaned_data.get('role')
        if role == 'student':
          user.is_student = True
        elif role == 'counselor':
          user.is_counselor = True

        if commit:
            user.save()

        return user
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control',}))
    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password', 'name': 'password',}))
