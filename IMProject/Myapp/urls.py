from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),          # root URL
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('student-dashboard/', views.student_dashboard_view, name='student_dashboard'),  # new
]
