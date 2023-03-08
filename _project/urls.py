from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),
    path("api/", include("students.urls")),
]
