from django.urls import path

from Portfolio import views

app_name = 'Portfolio'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', views.ProfileUpdateView.as_view(), name='Profile'),
    path('job/', views.JobCreate.as_view(), name='job_create'),
    path('job/update/<int:pk>', views.JobUpdate.as_view(), name='job_update'),
    path('job/remove/<int:pk>', views.JobDelete, name='job_delete'),
    path('skill/', views.SkillCreate.as_view(), name='skill_create'),
    path('skill/update/<int:pk>', views.SkillUpdate.as_view(), name='skill_update'),
    path('skill/remove/<int:pk>', views.SkillDelete, name='skill_delete'),
    path('education/', views.EducationCreate.as_view(), name='education_create'),
    path('education/update/<int:pk>', views.EducationUpdate.as_view(), name='education_update'),
    path('education/remove/<int:pk>', views.EducationDelete, name='education_delete'),
    path('language/', views.LanguageCreate.as_view(), name='language_create'),
    path('language/update/<int:pk>', views.LanguageUpdate.as_view(), name='language_update'),
    path('language/remove/<int:pk>', views.LanguageDelete, name='language_delete'),
    path('certificate/', views.CertificateCreate.as_view(), name='certificate_create'),
    path('certificate/update/<int:pk>', views.CertificateUpdate.as_view(), name='certificate_update'),
    path('certificate/remove/<int:pk>', views.CertificateDelete, name='certificate_delete'),
    path('', views.PortfolioView, name='portfolio')
]
