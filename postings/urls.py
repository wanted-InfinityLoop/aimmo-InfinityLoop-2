from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostingCreateView.as_view()),
    path("/<int:posting_id>", views.PostingView.as_view()),
    path("/list", views.PostingListView.as_view()),
]
