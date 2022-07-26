import os

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm

from .models import *

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username',)


class UploadForm(forms.Form):

    def validate_file_extension(value):
        from django.core.exceptions import ValidationError

        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.csv']
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Invalid file extension ')

    excel_file = forms.FileField(label='Excel File (.csv)', required=False, validators=[validate_file_extension])


class EntryForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'sex', 'phone', 'email')


class StaffRegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name', 'sex', 'phone',)


# class TestForm(ModelForm):
#     class Meta:
#         model = BloodTest
#         fields = ('hiv1', 'hiv2', 'maralia', 'hyperc')
# class AssignInvestigatorForm(ModelForm):
#     class Meta:
#         model = CaseInvestigator
#         fields = ('investigator',)
#
#
#
#
# class CaseForm(ModelForm):
#     class Meta:
#         model = Case
#         fields = ('crime', 'description',)
#
#
# class InvestigationReportForm(ModelForm):
#     class Meta:
#         model = InvestigationRecord
#         fields = ('status', 'description',)


class DateInput(forms.DateInput):
    input_type = 'date'
