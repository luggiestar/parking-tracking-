from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import *
from ..forms import *


# def donation(request):
#     donation = Donation.objects.all()
#     form = TestForm()
#
#     context = {
#         'donation': donation,
#         'form': form
#     }
#     return render(request, "admin/donation.html", context)

#
# def pending_donation(request):
#     donation = Donation.objects.all()
#     form = TestForm()
#
#     context = {
#         'donation': donation,
#         'form': form
#     }
#     return render(request, "admin/pending_donation.html", context)


# def save_test(request, donation_id):
#     donation = get_object_or_404(Donation, id=donation_id)
#     specialist = ZonalSpecialist.objects.filter(user=request.user).first()
#     if request.method == "POST":
#         form = TestForm(request.POST)
#         if form.is_valid():
#             get_form = form.save(commit=False)
#             get_form.donation = donation
#             get_form.specialist = specialist
#             get_form.save()
#             redirect('BLOOD:donation_result')
#
#     return redirect('BLOOD:donation')
#
#
# def donation_result(request):
#     donation_result = BloodTest.objects.all()
#
#     context = {
#         'donation_result': donation_result
#     }
#
#     return render(request, "admin/donation_result.html", context)
