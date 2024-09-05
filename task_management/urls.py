from django.contrib import admin
from django.urls import path, include

from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),  # Include task-related URLs
    path('', views.home, name='home'),  # Root URL pattern
]
