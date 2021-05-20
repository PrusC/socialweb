from django.http import request
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from .models import Photo, Comment
from .forms import NewPhotoForm
from likes.models import Like

class PhotoListView(ListView):
    model = Photo
    template_name = 'photo/all.html'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PhotoListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            photo_liked = [photo for photo in Photo.objects.all() if Like.is_user_liked(photo, self.request.user)]
            context['photo_liked'] = photo_liked
        return context


class PhotoDetail(DetailView):
    model = Photo
    template_name = 'photos/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PhotoDetail, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('date_created')
        return context


class PhotoCreate(LoginRequiredMixin, CreateView):
    model = Photo
    form_class = NewPhotoForm
    success_url = reverse_lazy('photos:detail')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PhotoCreate, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        return super(PhotoCreate, self).post(request, *args, **kwargs)


class PhotoDelete(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('account:home')