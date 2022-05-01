from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='jira_sub_tasks_home'),
    path('logout/', views.logout, name='logout'),
    path('privacy/', views.privacy, name='privacy'),
    path('backlog/', views.backlog, name='backlog'),
    path('landing/', views.landing, name='landing'),
    path('', views.login, name='login'),
]