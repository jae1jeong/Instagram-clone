from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from .views import SignUp,ProfileView,ProfileUpdate

app_name = "accounts"

urlpatterns = [
    path('login/',LoginView.as_view(template_name = "accounts/login.html"),name="login"),
    path('logout/',LogoutView.as_view(template_name = "accounts/logout.html"),name="logout"),
    path('signup/',SignUp,name="signup"),
    path('profile/<int:pk>/',ProfileView.as_view(),name="profile"),
    path("profile/update/<int:pk>",ProfileUpdate.as_view(), name="profile_update"),
]