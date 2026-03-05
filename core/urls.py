# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard_redirect_view
from . import views
from core import views as core_views

urlpatterns = [
    # หน้า Login มาตรฐานของ Django
    path('dashboard-redirect/', dashboard_redirect_view, name='dashboard_redirect'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('import-users/', views.import_users, name='import_users'),
    path('download-template/', views.download_user_template, name='download_user_template'),
    path('profile/', views.profile_view, name='profile'),
# หน้าสำหรับเปลี่ยนรหัสผ่าน
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='core/password_change_form.html'
    ), name='password_change'),

    # หน้าที่แสดงเมื่อเปลี่ยนรหัสสำเร็จ
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='core/password_change_done.html'
    ), name='password_change_done'),
]