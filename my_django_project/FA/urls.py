# 这些 URL 配置是在每个 Django 应用程序内部定义的，它们是名为 urls.py 的 Python 文件
from django.urls import path

from . import views
from .views import detect_face
from .views import save_face_encoding
from .views import check_attendance
from .views import require_lectures
from .views import show_absent_information
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('detect_face/', detect_face, name='detect_face'),
    path('save_face_encoding/', save_face_encoding, name='save_face_encoding'),
    path('check_attendance/', check_attendance, name='check_attendance'),
    path('require_lectures/', require_lectures, name='require_lectures'),
    path('show_absent_information/', show_absent_information, name='show_absent_information'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
