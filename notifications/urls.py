from django.urls import path
from . import views


urlpatterns = [
    path('line-webhook/', views.line_webhook, name='line_webhook'),
]