from django.urls import path, include 
from django.contrib import admin
from django.contrib.auth import views as auth_views
from users import views as user_views
"""The imports below are there for media"""
from django.conf import settings
from django.conf.urls.static import static 
"""The media imports end"""



"""This is the main urls file for the whole website"""
urlpatterns = [
    path('', include('blogs.urls', namespace='blogs')),
    path('admin/', admin.site.urls),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('paypal_pay/', include('payment.urls', namespace='payment')),
    # path('register/', user_views.register, name='register'),
    # path('profile/', user_views.profile, name='profile'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),
    #                            name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
                               name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
    	template_name='users/password_reset.html'),
                               name='reset_password'), 
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(
    	template_name='users/password_reset_done.html'),
                               name='password_reset_done'), 
    path('password_reset_comfirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    	template_name='users/password_reset_confirm.html'),
                               name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
      template_name='users/password_reset_complete.html'),
                               name='password_reset_complete'),

    # this is the allauth urls
    path('accounts/', include('allauth.urls')),






]

if settings.DEBUG:
	urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
