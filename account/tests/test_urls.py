from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account import views


class TestUrls(SimpleTestCase):

    def setUp(self) -> None:
        self.url = "account:"

    def test_account_login(self):
        url = reverse(self.url + 'login')
        self.assertEquals(resolve(url).func.view_class, views.UserLoginView)

    def test_account_logout(self):
        url = reverse(self.url + 'logout')
        self.assertEquals(resolve(url).func, views.logout_user)

    def test_account_register(self):
        url = reverse(self.url + 'register')
        self.assertEquals(resolve(url).func.view_class, views.UserCreateView)

    # def test_account_change(self):
    #     url = reverse(self.url + 'change')
    #     self.assertEquals(resolve(url).func.view_class, views)
    #
    # def test_account_reset(self):
    #     url = reverse(self.url + 'reset')
    #     self.assertEquals(resolve(url).func.view_class, views)
