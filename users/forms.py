from django import forms

from .models import CustomUser, Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'location',)
