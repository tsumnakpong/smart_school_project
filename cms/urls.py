from django.urls import path
from . import views
app_name = 'cms'
urlpatterns = [
    path('', views.home, name='home'),
    # --- ส่วนหน้าเว็บสำหรับบุคคลทั่วไป (Public) ---
    path('about/', views.about_view, name='about'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('curriculum/', views.curriculum_view, name='curriculum'),
    # --- ส่วนการจัดการเนื้อหา (Management - สำหรับครู/แอดมิน) ---
    # ใช้ HTMX หรือ Modal ที่คุณครูทำไว้มาจัดการตรงนี้ได้
    path('manage/news/', views.manage_news, name='manage_news'),
    path('manage/news/add/', views.news_create, name='news_create'),
    path('manage/news/<int:pk>/edit/', views.news_edit, name='news_edit'),
    path('manage/news/<int:pk>/delete/', views.news_delete, name='news_delete'),
    path('museum/', views.museum_view, name='museum'),
    path('online-learning/', views.learning_view, name='learning'),
    path('games/', views.games_view, name='games'),
    path('contact/', views.contact_view, name='contact'),
]