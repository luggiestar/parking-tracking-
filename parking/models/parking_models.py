from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from djmoney.models.fields import MoneyField

from django.conf import settings

User = settings.AUTH_USER_MODEL


class Brand(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        # unique_together = ('name', 'brand')
        verbose_name = "Car Brand"
        verbose_name_plural = "Car Brand"

    def __str__(self):
        return "{0}".format(self.name)


class Model(models.Model):
    name = models.CharField(max_length=40)
    brand = models.ForeignKey(Brand, on_delete=models.RESTRICT, related_name="car_brand")

    class Meta:
        unique_together = ('name', 'brand')
        verbose_name = "Car Model"
        verbose_name_plural = "Car Model"

    def __str__(self):
        return "{0}-{1}".format(self.name, self.brand)


class Fee(models.Model):
    amount = MoneyField("cost per hour",max_digits=14, decimal_places=2, default_currency='TZS', unique=True)
    description = models.CharField("number of second", max_length=100)

    class Meta:
        verbose_name = "Fee"
        verbose_name_plural = "Fee"

    def __str__(self):
        return "{0}-{1}".format(self.amount, self.description)


class Activity(models.Model):
    EVENTS = (
        ('ENTRANCE', 'ENTRANCE'),
        ('PARKING', 'PARKING'),
        ('EXIT', 'EXIT'),
    )

    event = models.CharField(max_length=40, choices=EVENTS, unique=True)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activity"

    def __str__(self):
        return "{0}".format(self.event)


class Car(models.Model):
    plate_regex = RegexValidator(regex=r"^(?=.{3,7}$)[T][0-9]{3}[A-Z]{3}",
                                 message="Invalid Plate Number, must be entered "
                                         "with the "
                                         "format: "
                                         "'T111AAA'")
    plate = models.CharField("Plate_Number", max_length=40, validators=[plate_regex], unique=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="car_model")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="car_owner")
    registered_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registered Car "
        verbose_name_plural = "Registered Cars"

    def __str__(self):
        return "{0}".format(self.plate)


class ParkingTracking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.RESTRICT, null=False,
                            related_name="tracked_car")
    activity = models.ForeignKey(Activity, on_delete=models.RESTRICT, null=True, blank=True,
                                 related_name="tracked_activity")
    activity_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parking Tracking"
        verbose_name_plural = "Parking Tracking"

    def __str__(self):
        return "{0}-{1}".format(self.car, self.activity)


class ParkingReport(models.Model):
    car = models.ForeignKey(Car, on_delete=models.RESTRICT, null=False,
                            related_name="parking_car_report")

    entrance = models.DateTimeField(null=True, blank=True)
    parking = models.DateTimeField(null=True, blank=True)
    exit = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    charge = MoneyField(max_digits=14, decimal_places=2, default_currency='TZS',default=0.00)

    class Meta:
        verbose_name = "Parking Report"
        verbose_name_plural = "Parking Report"

    def __str__(self):
        return "{0}-{1}".format(self.car, self.duration)

class ParkingCharge(models.Model):
    parking = models.ForeignKey(ParkingTracking, on_delete=models.RESTRICT, null=False,
                                related_name="parked_car")
    duration = models.DurationField(null=True, blank=True)
    charge = MoneyField(max_digits=14, decimal_places=2, default_currency='TZS')

    date = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     if self.description:
    #         self.charge=self.description. * self.charge.
    #
    #     return super(Donor, self).save(*args, **kwargs)
    class Meta:
        verbose_name = "Parking Charge"
        verbose_name_plural = "Parking Charge"

    def __str__(self):
        return "{0}-{1}".format(self.parking, self.charge)


class ParkingImport(models.Model):
    plate_regex = RegexValidator(regex=r"^(?=.{3,7}$)[T][0-9]{3}[A-Z]{3}",
                                 message="Invalid Plate Number, must be entered "
                                         "with the "
                                         "format: "
                                         "'T111AAA'")
    EVENTS = (
        ('ENTRANCE', 'ENTRANCE'),
        ('PARKING', 'PARKING'),
        ('EXIT', 'EXIT'),
    )
    plate = models.CharField("Plate_Number", validators=[plate_regex], max_length=100)
    activity = models.CharField(choices=EVENTS, max_length=100)
    is_valid=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parking Import"
        verbose_name_plural = "Parking Import"

    def __str__(self):
        return self.plate
