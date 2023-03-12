from django.urls import path
from . import views
import students.views
import copies.views

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<uuid:book_id>/", views.BookDetailView.as_view()),
    path("books/<uuid:book_id>/following/", students.views.FollowingView.as_view()),
    path("following/<int:following_id>/", students.views.FollowingDetailView.as_view()),
    path("copies/", copies.views.CopiesView.as_view()),
]
