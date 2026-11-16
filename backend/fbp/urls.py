from django.urls import path
from core import views
urlpatterns = [path("api/dashboard", views.dashboard)]
