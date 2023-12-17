from django.urls import path

from . import views


urlpatterns = [
    path("", views.W2WView.as_view(), name="w2w "),
    path("delay", views.W2WDelayView.as_view(), name="w2w with delay"),
]
