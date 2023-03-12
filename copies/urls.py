from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path("copies/", views.CopiesView.as_view()),
    path("borrow/", views.BorrowView.as_view()),
    path("borrow/<int:borrow_id>/devolution", views.BorrowDevolution.as_view()),
]
