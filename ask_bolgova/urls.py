from django.contrib import admin
from django.urls import path, include

from ask_bolgova import views

urlpatterns = [
    path('', views.index, name="index"),

]
