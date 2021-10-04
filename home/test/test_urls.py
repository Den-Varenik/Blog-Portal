from django.test import SimpleTestCase
from django.urls import reverse, resolve

from home import views


class TestHomeUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.url = 'home:'

    def test_category_list(self):
        url = reverse(self.url + 'category-list')
        self.assertEquals(resolve(url).func.view_class, views.CategoryListView)

    def test_post_list(self):
        url = reverse(self.url + 'post-list', args=["category_slug"])
        self.assertEquals(resolve(url).func.view_class, views.PostListView)

