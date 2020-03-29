from django.urls import path
from . import views

urlpatterns = [
    path('text/success/', views.TextSuccessView.as_view(), name='text_success'),
    path('text/', views.SendTextFormView.as_view(), name='send_text'),
    path('', views.home, name='home'),
]
