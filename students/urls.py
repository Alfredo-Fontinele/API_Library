from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path("students/", views.StudentView.as_view()),
    path("students/<uuid:student_id>/", views.StudentDetailView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
]
