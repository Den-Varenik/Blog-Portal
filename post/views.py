from django.http import Http404, JsonResponse
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import JSONResponseMixin, AjaxResponseMixin
from post.forms import PostForm, CommentForm
from post.models import Post, Category, Author, Comment, Like
from post.mixins import IsAuthorOrAdminMixin

from json import loads


class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    slug_url_kwarg = 'category_slug'
    paginate_by = 3

    def get_queryset(self):
        category_slug = self.kwargs[self.slug_url_kwarg]
        return Post.objects.filter(category__slug=category_slug).select_related('author').select_related('category')


class PostDetailView(AjaxResponseMixin, JSONResponseMixin, generic.DetailView):
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = "post"
    category = None
    http_method_names = ('get', 'post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm
        slug = self.kwargs[self.slug_url_kwarg]
        context["comments"] = Comment.objects.filter(post__slug=slug)
        return context

    def get(self, request, *args, **kwargs):
        category_slug = kwargs['category_slug']
        try:
            self.category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data_request = loads(request.read().decode('utf-8'))

            if "comment" in data_request and data_request["comment"] != '':
                slug = self.kwargs[self.slug_url_kwarg]
                post = Post.objects.get(slug=slug)

                if post is not None:
                    comment = Comment.objects.create(user=request.user, post=post, text=data_request["comment"])
                    comment.save()
                    data = {
                        'user': comment.user.username,
                        'active': comment.active,
                        'comment': comment.text,
                        'updated': comment.updated
                    }
                    return self.render_json_response(data)
        response = JsonResponse({"errors": "Ups, something go wrong..."})
        response.status_code = 405
        return response


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    login_url = reverse_lazy('account:login')

    def form_valid(self, form):
        author = Author.objects.get(user=self.request.user)

        form.instance.author = author
        form.save()
        return redirect(reverse("post:post-detail", kwargs={
            'category_slug': form.instance.category.slug,
            'post_slug': form.instance.slug
        }))


class PostUpdateView(IsAuthorOrAdminMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    slug_url_kwarg = 'post_slug'

    def form_valid(self, form):
        author = Author.objects.get(user=self.request.user)

        form.instance.author = author
        form.save()
        return redirect(reverse("post:post-detail", kwargs={
            'category_slug': form.instance.category.slug,
            'post_slug': form.instance.slug
        }))


class PostDeleteView(IsAuthorOrAdminMixin, generic.DeleteView):
    model = Post
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_success_url(self):
        post = Post.objects.get(slug=self.kwargs[self.slug_url_kwarg])
        return reverse_lazy('post:post-list', kwargs={
            'category_slug': post.category.slug
        })
