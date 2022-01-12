from django.shortcuts import redirect
from django.urls.base import reverse
from django.utils.deprecation import MiddlewareMixin


class StaffMiddleware(MiddlewareMixin):

    def __call__(self, request):

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user and request.user.is_staff is True and request.path.startswith('/student') is True:
            return redirect(reverse('admin:index'))

        if request.user and request.user.is_staff is False and request.path.startswith('/admin') is True:
            return redirect(reverse('quiz:home'))

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
