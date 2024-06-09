from django.urls import path

from . import views

app_name = 'NSO'

urlpatterns = [
   #Profile end points
   path('profile/', views.PProfile.as_view()),
   path('profile/<int:pk>/', views.GDPaProfile.as_view()),
   #Alias end points
   path('alias/', views.PAlias.as_view()),
   path('alias/<int:pk>/', views.GDPaAlias.as_view()),
   #Entry endpoints
   path('entry/', views.PEntry.as_view()),
   path('entry/<int:pk>/', views.PaEntry.as_view()),
   path('completeEntry/<int:pk>/', views.GDEntry.as_view()),
   path('entryList/', views.GEntries.as_view()),
]