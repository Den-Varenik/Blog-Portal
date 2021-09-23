from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from post import models, views


class PostTestCases(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="test",
                                             email="test@example.com",
                                             password="Test@123")
        self.category = models.Category.objects.create(name="coding", slug="code")
        image = SimpleUploadedFile("Python3.9.jpg", content=b'', content_type="image/jpg")
        self.post = models.Post.objects.create(author=self.user,
                                               title="All about Python3.9",
                                               slug="info-python3.9",
                                               body="Lorem ipsum",
                                               category=self.category,
                                               img=image)
        self.url = 'post:'

    def test_post_detail_GET(self):
        request = self.factory.get('')

        request.user = self.user
        response = views.PostDetailView.as_view()(request, category_slug=self.category.slug, post_slug=self.post.slug)
        self.assertEquals(response.status_code, 200)

        request.user = AnonymousUser()
        response = views.PostDetailView.as_view()(request, category_slug=self.category.slug, post_slug=self.post.slug)
        self.assertEquals(response.status_code, 200)

    def test_post_detail_POST(self):
        request = self.factory.post('')

        request.user = self.user
        response = views.PostDetailView.as_view()(request, category_slug=self.category.slug, post_slug=self.post.slug)
        self.assertEquals(response.status_code, 405)

        request.user = AnonymousUser()
        response = views.PostDetailView.as_view()(request, category_slug=self.category.slug, post_slug=self.post.slug)
        self.assertEquals(response.status_code, 405)

    def test_post_create_GET(self):  # TODO
        request = self.factory.get('')

        request.user = self.user
        response = views.PostCreateView.as_view()(request)
        self.assertEquals(response.status_code, 200)

        # request.user = AnonymousUser()
        # response = views.PostCreateView.as_view()(request)
        # self.assertEquals(response.status_code, 405)

    def test_post_create_POST(self):  # TODO
        pass

    def test_post_update_GET(self):  # TODO
        request = self.factory.get('')

        request.user = self.user
        response = views.PostUpdateView.as_view()(request, post_slug=self.post.slug)
        self.assertEquals(response.status_code, 200)

        # request.user = AnonymousUser()
        # response = views.PostUpdateView.as_view()(request, post_slug=self.post.slug)
        # self.assertEquals(response.status_code, 405)

    def test_post_update_PUT(self):  # TODO
        pass

    def test_post_delete_GET(self):  # TODO
        request = self.factory.get('')

        request.user = self.user
        response = views.PostDeleteView.as_view()(request, post_slug=self.post.slug)
        self.assertEquals(response.status_code, 200)

        # request.user = AnonymousUser()
        # response = views.PostDeleteView.as_view()(request, post_slug=self.post.slug)
        # self.assertEquals(response.status_code, 405)

    def test_post_delete_DELETE(self):  # TODO
        pass

    def test_category_list_GET(self):
        request = self.factory.get('')

        request.user = self.user
        response = views.PostListView.as_view()(request, category_slug=self.category.slug)
        self.assertEquals(response.status_code, 200)

        request.user = AnonymousUser()
        response = views.PostListView.as_view()(request, category_slug=self.category.slug)
        self.assertEquals(response.status_code, 200)

    def test_category_list_POST(self):
        request = self.factory.post('')

        request.user = self.user
        response = views.PostListView.as_view()(request, category_slug=self.category.slug)
        self.assertEquals(response.status_code, 405)

        request.user = AnonymousUser()
        response = views.PostListView.as_view()(request, category_slug=self.category.slug)
        self.assertEquals(response.status_code, 405)
