from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('profile/', views.ProfileList.as_view(), name='users'),
    path('profile/<slug:pk>/', views.Profile.as_view(), name='profile'),
    path('profile/update', views.UpdateProfile.as_view(), name='update_profile'),
    path('password/', views.PasswordChangeView.as_view(
        template_name="password_change.html"), name="change-password"),
]
