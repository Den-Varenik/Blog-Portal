from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from braces.views import JSONResponseMixin, AjaxResponseMixin
from post.forms import PostForm, CommentForm
from post import models
from post.mixins import IsAuthorOrAdminMixin

from json import loads


class PostDetailView(AjaxResponseMixin, JSONResponseMixin, generic.DetailView):
    model = models.Post
    slug_url_kwarg = 'post_slug'
    context_object_name = "post"
    category = None
    http_method_names = ('get', 'post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm
        slug = self.kwargs[self.slug_url_kwarg]
        context["comments"] = models.Comment.objects.filter(post__slug=slug).select_related('user')
        return context

    def post_ajax(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            data_request = loads(request.read().decode('utf-8'))

            if "comment" in data_request and data_request["comment"] != '':
                slug = self.kwargs[self.slug_url_kwarg]
                post = models.Post.objects.get(slug=slug)

                if post is not None:
                    comment = models.Comment.objects.create(user=request.user, post=post, text=data_request["comment"])
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
    model = models.Post
    form_class = PostForm
    login_url = reverse_lazy('account:login')

    def form_valid(self, form):
        author = models.Author.objects.get(user=self.request.user)

        form.instance.author = author
        form.save()
        return redirect(reverse("post:post-detail", kwargs={
            'category_slug': form.instance.category.slug,
            'post_slug': form.instance.slug
        }))


class PostUpdateView(IsAuthorOrAdminMixin, generic.UpdateView):
    model = models.Post
    form_class = PostForm
    slug_url_kwarg = 'post_slug'

    def form_valid(self, form):
        author = models.Author.objects.get(user=self.request.user)

        form.instance.author = author
        form.save()
        return redirect(reverse("post:post-detail", kwargs={
            'category_slug': form.instance.category.slug,
            'post_slug': form.instance.slug
        }))


class PostDeleteView(IsAuthorOrAdminMixin, generic.DeleteView):
    model =  models.Post
    context_object_name = "post"
    slug_url_kwarg = "post_slug"

    def get_success_url(self):
        post = models.Post.objects.get(slug=self.kwargs[self.slug_url_kwarg])
        return reverse_lazy('home:category-list', kwargs={
            'category_slug': post.category.slug
        })


class LikeView(LoginRequiredMixin, AjaxResponseMixin, JSONResponseMixin, generic.FormView):
    http_method_names = ('post',)
    slug_url_kwarg = 'post_slug'
    login_url = reverse_lazy('account:login')

    def post_ajax(self, request, *args, **kwargs):
        post = models.Post.objects.get(slug=self.kwargs[self.slug_url_kwarg])
        like, like_bool = models.Like.objects.get_or_create(user=request.user, post=post)
        if not like_bool:
            like.delete()
        return self.render_json_response({"likes": post.like.count()})
