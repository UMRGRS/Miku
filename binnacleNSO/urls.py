from django.urls import path, include

from . import views


app_name = 'NSO'

urlpatterns = [
   path('test/<int:pk>/', views.GallEntries.as_view()),
]