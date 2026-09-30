from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('profile')),  # Redirect homepage to profile
    path('', include('accounts.urls')),            # Loads signup, login, logout, profile
]