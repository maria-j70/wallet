from django.urls import path
from . import views


urlpatterns = [
    path('', views.DepositCreateView.as_view()),

]