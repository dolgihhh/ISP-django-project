from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
import random

class StudentExtra(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    course = models.CharField(max_length=40)
    faculty = models.CharField(max_length=40)

    def __str__(self):
        return self.user.first_name+' '+self.user.last_name+'['+str(self.course)+']'

    @property
    def get_name(self):
        return self.user.first_name+' '+self.user.last_name

    @property
    def getuserid(self):
        return self.user.id


def randomizer():
    while True:
        i = 0
        a = random.randint(0,1000000)
        books = Book.objects.all()
        for b in books:
            if b.unique_id == a:
                i += 1
        if i == 0:
            break
    return a


class Book(models.Model):
    catchoice= [
        ('фантастика', 'Фантастика'),
        ('детективы', 'Детективы'),
        ('комиксы', 'Комиксы'),
        ('биография', 'Биография'),
        ('историческая', 'Историческая'),
        ('научная', 'Научная'),
        ('классика', 'Классика'),
        ('триллер', 'Триллер'),
        ('роман', 'Роман'),
        ('психология','Психология'),
        ('детские', 'Детские'),
        ('учебная', 'Учебная')
        ]

    name = models.CharField(max_length=30)
    unique_id = models.PositiveIntegerField(default=randomizer)
    author = models.CharField(max_length=40)
    category = models.CharField(max_length=30,choices=catchoice,default='учебная')
    is_issued = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)+"["+str(self.unique_id)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)


class IssuedBook(models.Model):
    name = models.CharField(max_length=30)
    unique_id = models.CharField(max_length=30)
    issuedate = models.DateField(auto_now=True)
    expirydate = models.DateField(default=get_expiry)

    def __str__(self):
        return self.name