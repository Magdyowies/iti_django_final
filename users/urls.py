from django.urls import path
from .views import RegistrationView, ActivationView
from django.contrib.auth import views as auth_views
from .forms import AuthenticationForm

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', ActivationView.as_view(), name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=AuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
