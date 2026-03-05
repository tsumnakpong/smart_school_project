
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cms.urls', namespace='cms')),        # หน้าแรกคือ CMS
    path('core/', include('core.urls')),
    path('auth/', include('core.urls')),    # ระบบ Login
    path('sms/', include('sms.urls')),      # ระบบทะเบียน
    path('lms/', include('lms.urls', namespace='lms')),      # ระบบการเรียน
    path('iot/', include('iot.urls')),      # ระบบ AIoT API
    path('mis/', include('mis.urls', namespace='mis')), # ถ้ามี namespace='mis' ต้องเรียก mis:dashboard      # ระบบผู้บริหาร
    path('islamic/', include('islamic.urls', namespace='islamic')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_center=settings.MEDIA_ROOT)
