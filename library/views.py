from django.shortcuts import render


def home_view(request):
    return render(request,'index.html')


def studentclick_view(request):
    return render(request,'studentclick.html')


def adminclick_view(request):
    return render(request,'adminclick.html')