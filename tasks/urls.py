from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views
from .views import generate_and_upload_pdf, staff_task_list

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin login URL
    path('staff-login/', views.staff_login, name='staff_login'),  # Staff login URL
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/change-status/', views.change_task_status, name='change_task_status'),
    path('task/<int:pk>/', views.task_detail_public, name='task_detail_public'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Django's built-in logout view
    path('generate_and_upload_pdf/<str:mobile_number>/', generate_and_upload_pdf, name='generate_and_upload_pdf'),
    path('staff-tasks/', staff_task_list, name='staff_task_list'),  # Renamed to avoid confusion
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
