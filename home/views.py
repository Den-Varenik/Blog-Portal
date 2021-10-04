from django.views import generic
from post.models import Category, Post


class CategoryListView(generic.ListView):
    model = Category
    context_object_name = "categories"
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Список категорий"
        return context


class PostListView(generic.ListView):
    model = Post
    context_object_name = "posts"
    slug_url_kwarg = 'category_slug'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Посты категории"
        context["category"] = self.kwargs[self.slug_url_kwarg]
        return context

    def get_queryset(self):
        category_slug = self.kwargs[self.slug_url_kwarg]
        return Post.objects.filter(category__slug=category_slug)\
                           .select_related('author', 'category')\
                           .prefetch_related('like')
