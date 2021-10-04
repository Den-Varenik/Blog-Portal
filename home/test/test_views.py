from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser

from home import views
from post.models import Category


class HomeTestCase(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test",
                                             email="test@example.com",
                                             password="Test@123")
        self.category = Category.objects.create(name="coding", slug="code")

    def test_category_list_GET(self):
        request = self.factory.get('')

        request.user = self.user
        response = views.CategoryListView.as_view()(request)
        self.assertEquals(response.status_code, 200)

        request.user = AnonymousUser()
        response = views.CategoryListView.as_view()(request)
        self.assertEquals(response.status_code, 200)

    def test_post_list_GET(self):
        request = self.factory.get('')

        request.user = self.user
        response = views.PostListView.as_view()(request, category_slug=self.category.slug)
        self.assertEquals(response.status_code, 200)

        request.user = AnonymousUser()
        response = views.PostListView.as_view()(request, category_slug=self.category.slug)
        self.assertEquals(response.status_code, 200)
