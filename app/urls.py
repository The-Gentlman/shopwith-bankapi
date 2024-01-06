from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('register/', views.registerpage, name='register'),
    path('bankgateways/', views.go_to_gateway_view, name='pay'),

]
