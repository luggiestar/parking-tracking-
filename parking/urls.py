from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
app_name = 'parking'
urlpatterns = [
    path('', login_view, name="login"),
    # path('blood-donation/', donation, name="donation"),
    # path('pending-donation/', pending_donation, name="pending_donation"),
    # path('save-test/<donation_id>', save_test, name="save_test"),
    # path('donation-result/', donation_result, name="donation_result"),

    # apis
    path('data-api', ListParking.as_view()),
    path('<int:pk>/',DetailParking.as_view()),

]