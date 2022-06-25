from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

from .forms import *

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'first_name', 'middle_name', 'last_name', 'phone', 'sex', 'is_active',
                    'is_superuser', 'is_staff', 'is_active',)
    list_filter = ('username', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('personal', {'fields': ('first_name', 'middle_name', 'last_name', 'sex', 'phone','dob',),
                      }),

        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups',
                                    'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)


class BrandAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ['name', ]


admin.site.register(Brand, BrandAdmin)

class ModelAdmin(ImportExportModelAdmin):
    list_display = ('name', 'brand')
    search_fields = ['name', ]


admin.site.register(Model, ModelAdmin)


class FeeAdmin(ImportExportModelAdmin):
    list_display = ('amount', 'description')
    search_fields = ['amount', ]


admin.site.register(Fee, FeeAdmin)


class ActivityAdmin(ImportExportModelAdmin):
    list_display = ('event',)
    search_fields = ['event']
    # list_filter = ['title', 'station']

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(Activity, ActivityAdmin)


class CarAdmin(ImportExportModelAdmin):
    list_display = ('plate','model','owner','registered_on')
    search_fields = ['plate']
    list_filter = ['model','owner']

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(Car, CarAdmin)


class ParkingTrackingAdmin(ImportExportModelAdmin):
    list_display = ('car', 'activity','activity_date')
    search_fields = ['car']
    list_filter = ['car', 'activity']

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


admin.site.register(ParkingTracking, ParkingTrackingAdmin)


class ParkingChargeAdmin(ImportExportModelAdmin):
    list_display = ('parking', 'duration','charge','date')
    search_fields = ['parking']
    list_filter = ['parking']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(ParkingCharge, ParkingChargeAdmin)

class ParkingImportAdmin(ImportExportModelAdmin):
    list_display = ('plate', 'activity','is_valid','date')
    search_fields = ['plate']
    list_filter = ['plate']

    # def has_add_permission(self, request):
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(ParkingImport,ParkingImportAdmin)


