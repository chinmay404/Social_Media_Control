from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index_page,name='index_page'),
    path('login/',views.user_login,name='login'),
    path('logout/', views.user_logout, name='logout'),
]