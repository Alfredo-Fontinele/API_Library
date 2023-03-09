from django.urls import path
from . import views
import students.views 

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<uuid:book_id>/", views.BookDetailView.as_view()),
    path("books/<uuid:book_id>/following/",students.views.FollowingView.as_view()),
    path("following/<int:following_id>/",students.views.FollowingDetailView.as_view()),
]
