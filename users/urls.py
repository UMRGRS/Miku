from django.urls import path

from . import views

app_name = 'customUsers'

urlpatterns = [
    path('user/', views.PCustomUser.as_view()),
    path('user/<int:pk>/', views.GDPaCustomUser.as_view()),
    path('user/<int:pk>/password/', views.PuCustomUserPassword),
]