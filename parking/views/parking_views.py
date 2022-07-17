from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import *
from ..forms import *
import datetime


def parking_info(request):
    today = datetime.datetime.now().date()
    contexts = {
        'date': today,
    }
    return render(request, 'admin/parking.html', contexts)
