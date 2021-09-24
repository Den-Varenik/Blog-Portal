from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class IsAuthorOrAdminMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs[self.slug_url_kwarg]
        obj = self.model.objects.get(slug=slug)
        if request.user != obj.author or not request.user.is_staff:
            if request.user.is_authenticated:
                return redirect('home:index')
            else:
                return redirect('account:login')
        return super().dispatch(request, *args, **kwargs)
