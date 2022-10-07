
from turtle import title
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Post



class FeedView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'Polls/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = context['posts'].order_by('-id')
        
        search_input = self.request.GET.get('search-area')
        if search_input:
            # if search_input.lower() == 'oldest':
            #   context['notes'] = context['notes'].order_by('entry_date')
            #   return context
            context['posts'] = context['posts'].filter(post_text__icontains=search_input)
            return context
        else:
          return context


class MyPosts(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'Polls/myposts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = context['posts'].order_by('-id')
        context['posts'] = context['posts'].filter(user=self.request.user)
        
        search_input = self.request.GET.get('search-area')
        if search_input:
            # if search_input.lower() == 'oldest':
            #   context['notes'] = context['notes'].order_by('entry_date')
            #   return context
            context['posts'] = context['posts'].filter(post_text__icontains=search_input)
            return context
        else:
            return context


# class AccountPage(LoginRequiredMixin):
#     model = Bio
#     template_name = 'Polls/account.html'
#     context_object_name = 'bio'

#     def get_context_data(self, **kwargs):
#         myFeed = self.request.GET.get(MyPosts)

#         return super().get_context_data(**kwargs), myFeed

    



class ExploreView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'Polls/explore.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = context['posts'].order_by('-id')
        
        search_input = self.request.GET.get('search-area')
        if search_input:
            # if search_input.lower() == 'oldest':
            #   context['notes'] = context['notes'].order_by('entry_date')
            #   return context
            context['posts'] = context['posts'].filter(post_text__icontains=search_input)
            return context
        else:
          return context

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'Polls/add_post.html'
    fields = ['user', 'post_text']
    context_object_name = 'posts'
    success_url = reverse_lazy('Polls:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['user', 'post_text']
    template_name = 'Polls/edit_post.html'
    success_url = reverse_lazy('Polls:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostEdit, self).form_valid(form)


class ResultsView(DetailView):
    model = Post
    template_name = 'Polls/results.html'


class SignUpPage(FormView):
    template_name = 'Polls/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('Polls:home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUpPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('Polls:home')
        return super(SignUpPage, self).get(*args, **kwargs)


class SignInPage(LoginView):
    template_name = 'Polls/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('Polls:home')


class DeletePage(DeleteView):
    model = Post
    context_object_name = 'posts'
    template_name = 'Polls/del_post.html'
    success_url = reverse_lazy('Polls:home')