from django.urls import path
from . import views


urlpatterns = [
    path("", views.WithdrewCreateView.as_view()),
]
