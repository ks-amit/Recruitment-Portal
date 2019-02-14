from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.landing_view, name = 'landing'),
    path('login/', views.login_view, name = 'login'),
    path('signup/', views.signup_view, name = 'signup'),
    path('activate/', views.activate_view, name = 'activate'),
    path('forgot/', views.forgot_view, name = 'forgot'),
    path('reset/', views.reset_view, name = 'reset'),
]
