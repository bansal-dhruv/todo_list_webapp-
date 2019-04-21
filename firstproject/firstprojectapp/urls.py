from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('dashboard', views.dashboard),
    path('add_schedule', views.add),
    path('logout', views.logout),
    path('delete/<int:id>', views.delete),
    path('edit/<int:id>', views.edit),
    path('change/<int:id>', views.change)
]
