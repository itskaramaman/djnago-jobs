from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('sign-up/', views.sign_up, name="sign_up"),
    path('create-post/', views.create_post, name="create_post"),
    path('edit-post/<int:pk>/', views.edit_post, name="edit_post"),
    path('delete-post/<int:pk>/', views.delete_post, name="delete_post"),
    path('ban-user/<int:ban_user_pk>/', views.ban_user, name="ban_user"),
]
