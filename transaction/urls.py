from django.urls import path

from . import views


urlpatterns = [
    path('history/<wallet_id>', views.HistoryView.as_view()),

]
