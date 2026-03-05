from django.urls import path
from .views import CheckInAPI

urlpatterns = [
    path('api/checkin/', CheckInAPI.as_view(), name='api_checkin'),
]