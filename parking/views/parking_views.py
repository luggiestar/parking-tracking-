from http.client import HTTPResponse
from multiprocessing import context

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import *
from ..forms import *
import datetime


def parking_info(request):
    today = datetime.datetime.now().date()
    get_amount = ParkingCharge.objects.all().first()

    contexts = {
        'date': today,
        'today': get_amount,
    }
    return render(request, 'admin/parking.html', contexts)


@login_required(login_url='/user-authentication/')
def report_range(request):
    get_report = [];
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "GET":
            try:
                from_date = request.GET['date1']
                to_date = request.GET['date2']
                code = request.GET.get('complainant_code', False)
                get_report = ParkingReport.objects.filter(entrance__date__range=[from_date, to_date]).order_by('id')
                count_report = ParkingTracking.objects.filter(entrance__date__range=[from_date, to_date]).order_by('id').count()

                context = {
                    'report': get_report,
                    'count_report': count_report,
                    'from_date': from_date,
                    'to_date': to_date,
                }
                return render(request, 'admin/parking_history.html', context)
            except:
                context = {
                    'report': get_report
                }
                return render(request, 'admin/parking_history.html', context)
        context = {
            'report': get_report
        }
        return render(request, 'admin/parking_history.html', context)
    else:
        return redirect('parking:logout')