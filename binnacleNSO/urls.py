from django.urls import path, include

from . import views


app_name = 'NSO'

urlpatterns = [
   path('newProfile/', views.PProfile.as_view()),
]