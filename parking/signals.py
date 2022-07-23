# import datetime
import decimal
import json
# import time
import datetime
import time
import pytz
import requests

from django.db import transaction
from django.db.models import Sum

from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.http import request
from django.db.models import F

from .models import *


# User = settings.AUTH_USER_MODEL


def id_generator(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


#
# @receiver(post_save, sender=User, dispatch_uid='save_student_coursework')
# def calculate_student_semester_ca(sender, instance, created, raw=False, **kwargs):
#     if created and instance.title == "staff":
#         Complainant.objects.create(user=instance)

# @receiver(post_save, sender=ParkingImport, dispatch_uid='check_parking')
# def check_the_activitiy(sender, instance, created, raw=False, **kwargs):
#     # if created:
#     #     try:
#
#             if created and instance.activity == "PARKING":
#
#                     get_last_tracking = ParkingImport.objects.filter(plate=instance.plate).order_by('-id').first()
#                     if get_last_tracking.activity == "ENTRANCE":
#                         pass
#
#             elif created and instance.activity == "ENTRANCE":
#                 try:
#
#                     get_last_tracking = ParkingImport.objects.filter(plate=instance.plate).order_by('-id').first()
#                     if get_last_tracking.activity == "EXIT":
#                         pass
#                 except:
#                     instance.save()
#
#
#             elif created and instance.activity == "EXIT":
#
#
#                     get_last_tracking = ParkingImport.objects.filter(plate=instance.plate).order_by('-id').first()
#                     if get_last_tracking.activity == "PARKING":
#                         instance.save()

# except:
#     pass
#


@receiver(post_save, sender=ParkingImport, dispatch_uid='import_donors')
def import_donors(sender, instance, created, raw=False, **kwargs):
    if created:
        try:

            get_fee = Fee.objects.first()
            get_car = Car.objects.filter(plate=instance.plate).first()
            get_last_tracking = ParkingTracking.objects.filter(car=get_car).order_by('-id').first()
            car = get_last_tracking.car

            if instance.activity == "ENTRANCE":

                if get_last_tracking.activity.event == "EXIT":
                    get_event = Activity.objects.filter(event=instance.activity).first()

                    add_tracking = ParkingTracking(car=get_car,
                                                   activity=get_event,

                                                   )
                    add_tracking.save()
                    instance.is_valid = True
                    instance.save()
                # else:
                #     instance.is_valid = False
                #     instance.delete()
            if instance.activity == "PARKING":

                if get_last_tracking.activity.event == "ENTRANCE":
                    get_event = Activity.objects.filter(event=instance.activity).first()

                    add_tracking = ParkingTracking(car=get_car,
                                                   activity=get_event,

                                                   )
                    add_tracking.save()
                    instance.is_valid = True
                    instance.save()

            if instance.activity == "EXIT":

                if get_last_tracking.activity.event == "PARKING":
                    get_event = Activity.objects.filter(event=instance.activity).first()

                    add_tracking = ParkingTracking(car=get_car,
                                                   activity=get_event,

                                                   )
                    add_tracking.save()
                    instance.is_valid = True
                    instance.save()



        except:
            if instance.activity == "ENTRANCE":
                get_car = Car.objects.filter(plate=instance.plate).first()
                get_event = Activity.objects.filter(event=instance.activity).first()

                add_tracking = ParkingTracking(car=get_car,
                                               activity=get_event,

                                               )
                add_tracking.save()
                if add_tracking:
                    get_current = ParkingTracking.objects.filter(car=get_car).order_by(
                        '-id').first()
                    if get_current.activity.event == "ENTRANCE" or get_current.activity.event == "PARKING":
                        instance.is_valid = False
                        instance.save()
                    else:
                        instance.is_valid = True
                        instance.save()


@receiver(post_save, sender=ParkingTracking, dispatch_uid='check_tracking')
def check_tracking(sender, instance, created, raw=False, **kwargs):
    if created:
        try:

            get_fee = Fee.objects.first()
            get_last_tracking = ParkingTracking.objects.filter(car=instance.car).order_by(
                '-id')[1]
            car1 = get_last_tracking.car
            if instance.activity.event == "ENTRANCE":
                ParkingReport.objects.create(car=instance.car, entrance=instance.activity_date)
            if instance.activity.event == "PARKING":
                update_report = ParkingReport.objects.filter(car=instance.car).order_by('-id').first()
                update_report.parking = instance.activity_date
                update_report.save()

            # print(instance.activity.event == "EXIT" and get_last_tracking.activity.event == "PARKING")

            if instance.activity.event == "EXIT" and get_last_tracking.activity.event == "PARKING":
                get_latest_date = instance.activity_date
                get_last_date = get_last_tracking.activity_date
                diff = get_latest_date - get_last_date

                x = time.strptime(str(diff).split(',')[0], '%H:%M:%S.%f')
                gettt = (datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()) / 3600

                print(gettt)
                get_charges = get_fee.amount * decimal.Decimal(gettt)
                save_charge = ParkingCharge.objects.create(parking=instance, duration=diff, charge=get_charges)
                if save_charge:
                    update_report = ParkingReport.objects.filter(car=save_charge.parking.car).order_by('-id').first()
                    update_report.exit = save_charge.date
                    update_report.duration = save_charge.duration
                    update_report.charge = save_charge.charge
                    update_report.save()

        except:

            if instance.activity.event == "EXIT":
                instance.delete()

        # elif created and instance.activity == "PARKING":
        #
        #     get_last_tracking = ParkingImport.objects.filter(plate=instance.plate).order_by('-id').first()
        #     if get_last_tracking.activity == "ENTRANCE":
        #         get_event = Activity.objects.filter(event=instance.activity).first()
        #
        #         add_tracking = ParkingTracking(car=get_car,
        #                                        activity=get_event,
        #
        #                                        )
        #         add_tracking.save()
        #         instance.is_valid = True
        #         instance.save()
        #
        #
        #
        # elif created and instance.activity == "EXIT":
        #
        #     get_last_tracking = ParkingImport.objects.filter(plate=instance.plate).order_by('-id').first()
        #     if get_last_tracking.activity == "PARKING":
        #         get_event = Activity.objects.filter(event="EXIT").first()
        #         add_tracking = ParkingTracking(car=get_car,
        #                                        activity=get_event,
        #
        #                                        )
        #         add_tracking.save()
        #         instance.is_valid = True
        #         instance.save()
        #         if add_tracking:
        #             get_latest_date = instance.date
        #             get_last_date = get_last_tracking.activity_date
        #             diff = get_latest_date - get_last_date
        #
        #             x = time.strptime(str(diff).split(',')[0], '%H:%M:%S.%f')
        #             gettt = (datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()) / 3600
        #
        #             print(gettt)
        #             get_charges = get_fee.amount * decimal.Decimal(gettt)
        #             ParkingCharge.objects.create(parking=add_tracking, duration=diff, charge=get_charges)

        # if instance.activity == "EXIT" and get_last_tracking.activity.event == "PARKING":
        #
        #     get_latest_date = add_tracking.activity_date
        #     get_last_date = get_last_tracking.activity_date
        #     diff = get_latest_date - get_last_date
        #
        #     x = time.strptime(str(diff).split(',')[0], '%H:%M:%S.%f')
        #     gettt = (datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min, seconds=x.tm_sec).total_seconds()) / 3600
        #
        #     print(gettt)
        #     get_charges = get_fee.amount * decimal.Decimal(gettt)
        #     ParkingCharge.objects.create(parking=add_tracking, duration=diff, charge=get_charges)

        # get_import = DonorImport.objects.filter(id=instance.id).first()
        # get_import.delete()
#
# @receiver(post_save, sender=Student, dispatch_uid='create_registration_of_new_user')
# def create_registration(sender, instance, created, **kwargs):
#     if created:
#         get_status = Status.objects.get(code="NOT PAID")
#         get_semester = AcademicSemester.objects.filter(is_active=True).first()
#         save_registration = Registration(student=instance, level=instance.entry_level, status=get_status,
#                                          semester=get_semester)
#         save_registration.save()
#
#         URL = 'https://apisms.beem.africa/v1/send'
#         api_key = '2799f1a807695012'
#         secret_key = 'YTU2NTkxZjQxZDc4NTY2NGZiZTVkYzI5ZWU1MzFmYzM4NzA4MTBkYjk5NWE4MzZmZmU0MjQ2OTU3YjJjN2IxZg===='
#         content_type = 'application/json'
#         source_addr = 'KAHAMA COLL'
#         apikey_and_apisecret = api_key + ':' + secret_key
#
#         '''Get name and concatenate them'''
#         first_name = instance.user.first_name
#         last_name = instance.user.last_name
#         full_name = f"{first_name} {last_name}"
#
#         '''Get amount invested and daily amount earning'''
#         program = instance.programme
#         username = instance.user.username
#         password = last_name
#
#         '''Get phone detail and convert and user id as recipient_id on api'''
#         # number= "255755422199"
#         phone = str(instance.user.phone)
#         # phone = str(number)
#         phone = phone[1:10]
#         # phone = phone
#         phone = '255' + phone
#
#         user_id = instance.id
#
#         message_body = f"Congratulation,Dear {full_name}, \nyou have been selected to join KAHAMA COLLEGE OF HEALTH " \
#                        f"SCIENCE to pursue {program}\n please login to our system through \n " \
#                        f"https://kachs.herokuapp.com/login to proceed with  " \
#                        f"registration\n username:{username},\n password:{password} "
#
#         print(message_body)
#         first_request = requests.post(url=URL, data=json.dumps({
#             'source_addr': source_addr,
#             'schedule_time': '',
#             'encoding': '0',
#             'message': message_body,
#             'recipients': [
#                 {
#                     'recipient_id': user_id,
#                     'dest_addr': phone,
#                 },
#             ],
#         }),
#
#                                       headers={
#                                           'Content-Type': content_type,
#                                           'Authorization': 'Basic ' + api_key + ':' + secret_key,
#                                       },
#
#                                       auth=(api_key, secret_key), verify=False)
#
#         print(first_request.status_code)
#         if first_request.status_code == 200:
#             full_name = ''
#             phone = ''
#         print(first_request.json())
#
#         # return (first_request.json())


#
# @receiver(post_save, sender=Type, dispatch_uid='create_payment_structure')
# def create_payment_structure_total(sender, instance, created, **kwargs):
#     if created:
#         get_ordinary_level = Level.objects.get(name="O-Level")
#         get_advanced_level = Level.objects.get(name="A-Level")
#
#         PaymentStructure.objects.create(type=instance, level=get_ordinary_level)
#         PaymentStructure.objects.create(type=instance, level=get_advanced_level)

# @receiver(post_save, sender=Payment, dispatch_uid='update_balance')
# def update_remaining_fee_amount(sender, instance, created, **kwargs):
#     if created:
#         get_latest_balance = InvestmentTracking.objects.filter(
#             investment__account__code=instance.investment.account.invite).order_by(
#             '-id').first()
#         get_user = Investment.objects.filter(account__code=instance.investment.account.invite).order_by('-id').first()
#
#         # print(get_latest_balance.balance)
#
#         save_balance = InvestmentTracking(
#             investment=get_user,
#             total_referral=get_latest_balance.total_referral + decimal.Decimal(float(instance.amount)),
#             total_earning=get_latest_balance.total_earning,
#             total_withdraw=get_latest_balance.total_withdraw,
#
#             balance=get_latest_balance.balance + instance.amount
#         )
#         save_balance.save()
