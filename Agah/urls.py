from django.urls import path
from Agah import views

urlpatterns = [
    path('personal/', views.Personal, name='personal'),
    path('children/', views.Children, name='children'),
    path('main/', views.Main_view, name='main'),
]
