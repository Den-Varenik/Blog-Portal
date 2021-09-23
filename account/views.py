from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from account.forms import RegisterUserForm, LoginUserForm


class UserCreateView(generic.CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy("account:login")
    template_name = 'account/user_form.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home:index')


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'account/user_form.html'

    def get_success_url(self):
        return reverse_lazy("home:index")


@login_required
def logout_user(request):
    logout(request)
    return redirect('account:login')
