from django.shortcuts import render
from . import forms, models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from .models import Book
import logging
import asyncio
from library.async_requests import *

logger = logging.getLogger(__name__)


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'index.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'studentclick.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'adminclick.html')


def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()
            logger.info(f'{user} registred')
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request, 'studentsignup.html', context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def afterlogin_view(request):
    if is_admin(request.user) or request.user.username == "admin":
        logger.info(f'{request.user.username} logged in')
        return render(request, 'adminafterlogin.html')
    else:
        logger.info(f'{request.user.username} logged in')
        return render(request, 'studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form = forms.BookForm()
    if request.method == 'POST':
        form = forms.BookForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f'{user} book added')
            return render(request, 'bookadded.html')
    return render(request, 'addbook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    all_books = get_all_books(request)
    return asyncio.run(all_books)

    # books = models.Book.objects.filter(is_issued=False)
    # return render(request, 'viewbook.html', {'books': books})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    all_students = get_all_students(request)
    return asyncio.run(all_students)

    # students = models.StudentExtra.objects.all()
    # return render(request, 'viewstudent.html', {'students': students})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.unique_id = request.POST.get('book2')
            obj.enrollment = request.POST.get('enrollment2')
            book = Book.objects.get(unique_id=obj.unique_id)
            obj.name = book.name
            book.is_issued = True
            book.save()
            logger.info(f'{book} issued')
            obj.save()
            return render(request, 'bookissued.html')
    return render(request, 'issuebook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    li = []
    for ib in issuedbooks:
        issdate = str(ib.issuedate.day) + '.' + str(ib.issuedate.month) + '.' + str(ib.issuedate.year)
        expdate = str(ib.expirydate.day) + '.' + str(ib.expirydate.month) + '.' + str(ib.expirydate.year)
        # fine calculation
        days = (date.today() - ib.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d - 15
            fine = day * 10

        books = list(models.Book.objects.filter(unique_id=ib.unique_id))
        students = list(models.StudentExtra.objects.filter(user_id=ib.enrollment))
        i = 0
        for l in books:
            t = (students[i].get_name, students[i].course, students[i].faculty, books[i].name,
                 books[i].author, books[i].unique_id, issdate, expdate, fine)
            i = i + 1
            li.append(t)

    return render(request, 'viewissuedbook.html', {'li': li})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook = models.IssuedBook.objects.filter(enrollment=student[0].user_id)

    li1 = []

    li2 = []
    for ib in issuedbook:
        books = models.Book.objects.filter(unique_id=ib.unique_id)
        for book in books:
            t = (book.name, book.author)
            li1.append(t)
        issdate = str(ib.issuedate.day) + '.' + str(ib.issuedate.month) + '.' + str(ib.issuedate.year)
        expdate = str(ib.expirydate.day) + '.' + str(ib.expirydate.month) + '.' + str(ib.expirydate.year)
        # fine calculation
        days = (date.today() - ib.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d - 15
            fine = day * 10
        t = (issdate, expdate, fine)
        li2.append(t)

    return render(request, 'viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})
