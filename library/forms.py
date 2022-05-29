from django import forms
from django.contrib.auth.models import User
from . import models


class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']


class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['course','faculty']


class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['name','author','category']