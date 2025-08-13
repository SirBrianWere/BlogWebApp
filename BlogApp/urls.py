from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from gallery.views import CustomPasswordResetView, registration_view
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView
from gallery.token import password_reset_token
from gallery.views import CustomLoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', registration_view, name='register'),
    path('accounts/logout/', LogoutView.as_view(http_method_names=['get', 'post']), name='logout'),

    #Password Reset URLS
    path('accounts/reset-password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/reset-password/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('accounts/reset-password/confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             token_generator=password_reset_token,
             template_name='registration/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('accounts/reset-password/complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    #Blog URLS
    path('blog/', include('gallery.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)