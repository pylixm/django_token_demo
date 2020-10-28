from django.contrib import admin
from django.urls import path
from managerapp.views import UserView, LoginView

urlpatterns = [
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
]
