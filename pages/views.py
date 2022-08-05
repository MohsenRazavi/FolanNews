from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from .models import Post
from .forms import NewPostForm


class HomePageView(generic.ListView):
    template_name = 'pages/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(status='pub').order_by('-datetime_lastedit')


class PostDetailView(generic.DetailView):
    template_name = 'pages/detail.html'
    context_object_name = 'post'
    model = Post


def AboutPageView(request):
    return render(request, 'pages/about.html')


def ContactPageView(request):
    return render(request, 'pages/contact.html')


class NewPostView(generic.CreateView):
    model = Post
    template_name = 'pages/new_post.html'
    form_class = NewPostForm


class EditPostView(generic.UpdateView):
    model = Post
    template_name = 'pages/edit_post.html'
    form_class = NewPostForm

class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'pages/delete_post.html'
    success_url = reverse_lazy('home')
