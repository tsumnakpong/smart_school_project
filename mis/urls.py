# mis/urls.py
from django.urls import path
from .views import ExecutiveDashboardView
app_name = 'mis'
urlpatterns = [
    # ตั้งชื่อ name ให้ตรงกับที่ใช้ใน redirect ของ core/views.py
    path('dashboard/', ExecutiveDashboardView.as_view(), name='executive_dashboard'),
]