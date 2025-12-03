from django.urls import path
from api.views import auth_views, admin_views

urlpatterns = [
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('register/', auth_views.register_view, name='register'),
    path('set-password/<str:unique_identifier>/', auth_views.set_password, name='set_password'),
    path('forgot-password/', auth_views.forgot_password, name='forgot_password'),
    path('check-auth/', auth_views.check_auth, name='check_auth'),
    
    path('profile/', auth_views.profile_view, name='profile'),
    path('profile/update/', auth_views.update_profile, name='update_profile'),
    path('profile/delete/', auth_views.delete_account, name='delete_account'),
    
    path('admin/registrations/', admin_views.admin_registrations_view, name='admin_registrations'),
    path('admin/users/', admin_views.admin_users_view, name='admin_users'),
    path('admin/users/<str:action>/', admin_views.admin_user_action, name='admin_user_action'),
]
