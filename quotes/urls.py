from django.urls import path
from . import views

urlpatterns = [
    path('text/success/', views.TextSuccessView.as_view(), name='text_success'),
    path('text/', views.SendTextFormView.as_view(), name='send_text'),
    path('sms/', views.handle_inbound_sms, name='handle_inbound_sms'),
    path('voice/', views.handle_inbound_calls, name='handle_inbound_calls'),
    path('', views.HomeView.as_view(), name='home'),
]
