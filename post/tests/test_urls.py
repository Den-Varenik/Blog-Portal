from django.test import SimpleTestCase
from django.urls import reverse, resolve
from post import views


class TestPostUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.url = 'post:'

    def test_post_detail(self):
        url = reverse(self.url + 'post-detail', args=['post_slug'])
        self.assertEquals(resolve(url).func.view_class, views.PostDetailView)

    def test_post_create(self):
        url = reverse(self.url + 'post-create')
        self.assertEquals(resolve(url).func.view_class, views.PostCreateView)

    def test_post_update(self):
        url = reverse(self.url + 'post-update', args=['post_slug'])
        self.assertEquals(resolve(url).func.view_class, views.PostUpdateView)

    def test_post_delete(self):
        url = reverse(self.url + 'post-delete', args=['post_slug'])
        self.assertEquals(resolve(url).func.view_class, views.PostDeleteView)

    # def test_category_list(self):
    #     url = reverse(self.url + 'post-list', args=['category_slug'])
    #     self.assertEquals(resolve(url).func.view_class, views.PostListView)

