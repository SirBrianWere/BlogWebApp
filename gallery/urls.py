from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import registration_view 
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.product_list, name='product_list'),
    path('discover/', views.discover_posts, name='discover'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('register/', registration_view, name='register'),
    path('create/', views.create_product, name='create_product'), #CREATE
    path('logout/', LogoutView.as_view(http_method_names=['get', 'post'], next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('<slug:slug>/', login_required(views.product_detail), name='product_detail'), #READ
    path('<slug:slug>/edit/', views.edit_product, name='edit_product'), #EDIT/UPDATE
    path('<slug:slug>/delete/', views.delete_product, name='delete_product'), #DELETE
    path('like/<slug:slug>/', views.like_post, name='like_post'),
]