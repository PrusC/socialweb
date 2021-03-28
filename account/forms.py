from django import forms
from django.contrib.auth import password_validation
# from django.contrib.auth.forms import UserCreationForm
from . import models

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html()
        )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter your password once more"
        )

    class Meta:
        model = models.USER_MODEL
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        # cd = self.cleaned_data
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The two password fields didn’t match.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = True
        if commit:
            user.save()
        return user
