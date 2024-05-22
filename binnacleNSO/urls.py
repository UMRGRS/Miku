from django.urls import path, include

from . import views


app_name = 'NSO'

urlpatterns = [
   #Profiles end points
   path('createProfile/', views.PProfile.as_view()),
   path('updateProfile/<int:pk>/', views.PaProfile.as_view()),
   path('getProfile/<int:pk>/', views.GDProfile.as_view()),
   path('deleteProfile/<int:pk>/', views.GDProfile.as_view()),
   #Aliases end points
   path('createAlias/', views.PAlias.as_view()),
   path('updateAlias/<int:pk>/', views.GPaAlias.as_view()),
   path('getAlias/<int:pk>/', views.GPaAlias.as_view()),
   path('deleteAlias/<int:pk>/', views.DAlias.as_view()),
   #Entries endpoints
   path('createEntry/', views.PEntry.as_view()),
   path('updateEntry/<int:pk>/', views.GPaEntry.as_view()),
   path('getEntry/<int:pk>/', views.GPaEntry.as_view()),
   path('getUserEntries/<int:pk>/', views.GallEntries.as_view()),
]