from asgiref.sync import sync_to_async
from django.db import models
from django.shortcuts import render
from . import forms, models


@sync_to_async
def get_all_books(request):
    books = models.Book.objects.filter(is_issued=False)
    return render(request, 'viewbook.html', {'books': books})


@sync_to_async
def get_all_students(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'viewstudent.html', {'students': students})
