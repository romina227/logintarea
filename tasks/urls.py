from django.urls import path
from . import views
app_name = 'tasks'

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('create/', views.create, name='create'),
    path('account/', views.account_detail, name='account_detail'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'), 
    path('logout/', views.logout_view, name='logout'),
    path('detail/<int:task_id>/', views.detail, name='detail'),
    path('edit/<int:task_id>/', views.edit, name='edit'),
    path('delete/<int:task_id>/', views.delete, name='delete'),
]