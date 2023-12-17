from django.urls import path

from . import views


urlpatterns = [
    path('', views.WalletListCreate.as_view(), name='wallet list'),
    path('<wallet_id>', views.WalletRetrieveDestroyView.as_view(), name='wallet list'),
]

