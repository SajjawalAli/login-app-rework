from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Explicitly specify the backend since django-axes is installed
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'accounts/profile.html')