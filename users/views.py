from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import UserForm, UserProfileForm

# Create your views here.
@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!', extra_tags='alert alert-success')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.', extra_tags='alert alert-danger')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    return render(request, 'account/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
