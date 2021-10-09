from django.urls import path

from Portfolio import views

app_name = 'Portfolio'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', views.ProfileUpdateView.as_view(), name='Profile'),
    path('job/', views.JobCreate.as_view(), name='job_create'),
    path('portfolio/', views.PortfolioView, name='portfolio'),
]
