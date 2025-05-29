from django.urls import path
from . import views

urlpatterns = [
    path('webhook/bank/', views.handle_bank_webhook, name='handle_bank_webhook'),
    path('organizations/<str:inn>/balance/', views.get_organization_balance, name='get_organization_balance'),
]