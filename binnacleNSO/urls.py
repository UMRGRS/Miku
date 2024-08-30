from django.urls import path
from . import views

app_name = 'binnacleNSO'

urlpatterns = [
    # Alias endpoints
    path('alias/', views.CreateAlias.as_view()),
    path('alias/<int:pk>/', views.SeeUpdateDeleteAlias.as_view()),
    path('alias-list/', views.ListAlias.as_view()),
    # Entry endpoints
    path('entry/', views.CreateEntry.as_view()),
    path('entry/<int:pk>/', views.UpdateEntry.as_view()),
    path('entry-detail/<int:pk>/', views.SeeDeleteEntry.as_view()),
    path('entry-list/', views.ListEntries.as_view()),
]