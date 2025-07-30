from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import registration_view 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.product_list, name='product_list'),
    path('register/', registration_view, name='register'),
    path('<int:pk>/', login_required(views.product_detail), name='product_detail'), #READ
    path('create/', views.create_product, name='create_product'), #CREATE
    path('<int:pk>/edit/', views.edit_product, name='edit_product'), #EDIT
    path('<int:pk>/delete/', views.delete_product, name='delete_product'), #DELETE
    path('logout/', LogoutView.as_view(), name='logout'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
]