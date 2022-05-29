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


class IssuedBookForm(forms.Form):

    book2=forms.ModelChoiceField(queryset=models.Book.objects.filter(is_issued=False),empty_label="Название и уникальный номер", to_field_name="unique_id",label='Название и уникальный номер')
    enrollment2=forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(),empty_label="Имя и курс", to_field_name="user_id",label='Имя и курс')
