from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('short_link.urls')),
    path('admin/', admin.site.urls),
]
