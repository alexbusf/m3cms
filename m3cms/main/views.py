from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .models import Post, User, Category
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q


class PostListView(generic.ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published=True)


class PostByCategoryView(generic.ListView):
    model = Post

    def get_queryset(self):
        cat = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Post.objects.filter(category=cat, published=True)
        #return Post.objects.filter(category__slug=self.kwargs['category_slug'])


class PostByAuthorView(generic.ListView):
    model = Post

    def get_queryset(self):
        auth = get_object_or_404(User, pk=self.kwargs['pk'])
        return Post.objects.filter(author=auth)


class SearchResultsView(generic.ListView):
    model = Post

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        return object_list



class PostDetail(generic.DetailView):
    model = Post


class About(generic.TemplateView):
    template_name = 'main/about.html'


class PostCreateView(PermissionRequiredMixin, generic.edit.CreateView):
    model = Post
    template_name = 'main/post_create.html'
    fields = ['title', 'category', 'description', 'content', 'published']
    permission_required = 'main.can_post_create_edit'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.save()
        return super().form_valid(form)


class PostUpdateView(PermissionRequiredMixin, generic.edit.UpdateView):
    model = Post
    template_name = 'main/post_update.html'
    fields = ['title', 'category', 'description', 'content', 'published']
    permission_required = 'main.can_post_create_edit'


class PostDeleteView(PermissionRequiredMixin, generic.edit.DeleteView):
    model = Post
    template_name = 'main/post_delete.html'
    success_url = reverse_lazy('post-list')
    permission_required = 'main.can_post_delete'


class UserLogin(LoginView):
    template_name = 'registration/login.html'


