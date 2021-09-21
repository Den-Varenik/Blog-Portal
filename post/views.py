from django.shortcuts import redirect, reverse
from django.views import generic
from django.http import Http404
from post.models import Post, Category
from post.forms import PostCreateForm

#__all__ = [
#     'View', 'TemplateView', 'RedirectView', 'ArchiveIndexView',
#     'YearArchiveView', 'MonthArchiveView', 'WeekArchiveView', 'DayArchiveView',
#     'TodayArchiveView', 'DateDetailView', 'DetailView', 'FormView',
#     'CreateView', 'UpdateView', 'DeleteView', 'ListView', 'GenericViewError',
# ]


class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    slug_url_kwarg = 'category_slug'
    paginate_by = 1

    def get_queryset(self):
        category_slug = self.kwargs[self.slug_url_kwarg]
        return Post.objects.filter(category__slug=category_slug)


class PostDetailView(generic.DetailView):
    model = Post
    slug_url_kwarg = 'post_slug'
    context_object_name = "post"
    category = None

    def get(self, request, *args, **kwargs):
        category_slug = kwargs['category_slug']
        try:
            self.category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
        return super().get(request, *args, **kwargs)


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return redirect(reverse("post:post-detail", kwargs={
            'category_slug': form.instance.category.slug,
            'post_slug': form.instance.slug
        }))
