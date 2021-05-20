import django
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth import mixins as auth_mixins
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
# from django import forms
from django.views.generic.edit import DeleteView

from . import forms
from . import models

from photos.models import Photo, Comment

from weather.views import get_weather


def _get_form_errors(form):
    res = list()
    for value in form.errors.as_data().values():
        for error in value:
            for e in error.messages:
                res.append(str(e))
    return res

def _get_main_page(request, form_login=None, form_registration=None):
    if form_login is None:
        form_login = forms.LoginForm()
    if form_registration is None:
        form_registration = forms.UserRegistrationForm()
    context = {'form_login': form_login, "form_registration": form_registration}
    context.update(get_weather(request, 'Moscow'))
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
            str_message = _("Login or Password doesn't correct")
            messages.add_message(request, messages.ERROR, str_message)
            return _get_main_page(request, form_login=form_login)

    form_registration = forms.UserRegistrationForm(request.POST)
    if form_registration.is_valid():
        user = form_registration.save()
        username = form_registration.cleaned_data.get('username')
        messages.success(request, _(f'Your account has been created! You can now login!'))
        login(request, user)
        return redirect('account:edit')

    else:
        for error in _get_form_errors(form_registration):
            messages.error(request, _(error))
        return _get_main_page(request, form_registration=form_registration)


def main_page(request):
    if request.method == 'POST':
        return _post_main_page(request)
    else:
        if request.user.is_authenticated:
            return redirect('account:profile')
        else:
            return _get_main_page(request)


@login_required
def profile(request):
    user = request.user
    profile = user.profile
    photos = Photo.get_photos_by_user(user)
    photos_count = photos.count()
    context = {
        'profile': profile,
        'is_my_profile': True,
        'photos_count': photos_count,
        'photos': photos,
    }
    return render(request, 'account/profile.html', context=context)


class UserLogoutView(auth_mixins.LoginRequiredMixin, auth_views.LogoutView):
    redirect_field_name = 'account/main_page.html'


class UserDeleteView(auth_mixins.LoginRequiredMixin, DeleteView):
    model = models.USER_MODEL
    template_name = 'account/delete_user.html'
    success_url = reverse_lazy('account:main_page')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'User has been deleted')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
        

@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = forms.UserForm(request.POST, instance=request.user)
        profile_form = forms.ProfileForm(
            request.POST, 
            instance=request.user.profile,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile has been updated'))

        else:
            for error in _get_form_errors(profile_form):
                messages.error(request, _(error))
        # elif not profile_form.cleaned_data['slug']:
        #     messages.error(request, _("The user with this Id already exists"))
        # else:
        #     messages.error(request, _('Correct your input data'))
    
    else:
        user_form = forms.UserForm(instance=request.user)
        profile_form = forms.ProfileForm(instance=request.user.profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'account/edit.html', context)
