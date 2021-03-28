from django.shortcuts import redirect, render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth import mixins as auth_mixins
from django.urls.base import reverse
from django.contrib import messages

from . import forms


def _get_main_page(request):
    form_login = forms.LoginForm()
    form_registration = forms.UserRegistrationForm()
    context = {'form_login': form_login, "form_registration": form_registration}
    return render(request, 'account/main_page.html', context)

def _post_main_page(request):
    form_login = forms.LoginForm(request.POST)
    if form_login.is_valid():
        cd = form_login.cleaned_data
        username = cd['username']
        password = cd['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse("account:profile"))
        else:
            str_message = "Login or Password doesn't correct"
            messages.add_message(request, messages.ERROR, str_message)
            return _get_main_page(request)

    form_registration = forms.UserRegistrationForm(request.POST)
    if form_registration.is_valid():
        form_registration.save()
        username = form_registration.cleaned_data.get('username')
        messages.success(request, f'Your account has been created! You can now login!')
        return redirect('account:profile')

def main_page(request):
    if request.method == 'POST':
        return _post_main_page(request)
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("account:profile"))
        else:
            return _get_main_page(request)


def  profile(request):
    return render(request, 'account/profile.html')


class UserLogoutView(auth_mixins.LoginRequiredMixin, auth_views.LogoutView):
    redirect_field_name = 'account/main_page.html'