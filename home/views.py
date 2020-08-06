from django.http import HttpResponse
from django.shortcuts import render

from home.models import Setting


def index(request):
    setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()
    context = {
        "setting": setting
    }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()
    context = {
        "setting": setting
    }
    return render(request, 'hakkimizda.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    # category = Category.objects.all()
    context = {
        "setting": setting
    }
    return render(request, 'referanslar.html', context)
