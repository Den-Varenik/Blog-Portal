from django.http import Http404
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views import generic

from post.forms import PostForm
from post.models import Post, Category


class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    slug_url_kwarg = 'category_slug'
    paginate_by = 3

    def get_queryset(self):
        category_slug = self.kwargs[self.slug_url_kwarg]
        return Post.objects.filter(category__slug=category_slug).select_related('author').select_related('category')


class PostDetailView(generic.DetailView):
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = "post"
    category = None

    def get_queryset(self, *args, **kwargs):
        post_slug = self.kwargs[self.slug_url_kwarg]
        return Post.objects.filter(slug=post_slug).select_related('author')

    def get(self, request, *args, **kwargs):
        category_slug = kwargs['category_slug']
        try:
            self.category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse("post:post-detail", kwargs={
            'category_slug': form.instance.category.slug,
            'post_slug': form.instance.slug
        }))


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    slug_url_kwarg = 'post_slug'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse("post:post-detail", kwargs={
            'category_slug': form.instance.category.slug,
            'post_slug': form.instance.slug
        }))


class PostDeleteView(generic.DeleteView):
    model = Post
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_success_url(self):
        post = Post.objects.get(slug=self.kwargs[self.slug_url_kwarg])
        return reverse_lazy('post:post-list', kwargs={
            'category_slug': post.category.slug
        })
