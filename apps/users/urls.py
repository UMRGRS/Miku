from django.urls import path
from knox import views as knox_views

from . import views

app_name = 'Users'

urlpatterns = [
    path(r'user-new/', views.Signup.as_view()),
    path(r'user/', views.SeeUser.as_view()),
    path(r'user/<int:pk>/', views.UpdateDeleteUser.as_view()),
    path(r'login/', views.LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(r'logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]