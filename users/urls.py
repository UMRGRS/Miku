from django.urls import path
from knox import views as knox_views

from . import views

app_name = 'Users'

urlpatterns = [
    path('user/', views.Signup.as_view()),
    path('user/<int:pk>/', views.SeeUpdateDeleteUser.as_view()),
    path(r'login/', views.LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]