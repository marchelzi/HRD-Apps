from functools import wraps

from django.http import HttpResponseRedirect


def is_authenticated(f):
    wraps(f)

    def wrapped(request, *args, **kwargs):
        """Redirect to login if user is not authenticated in .

        Args:
            request ([type]): [description]

        Returns:
            [type]: [description]
        """
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/auth/login")
        else:
            return f(request, *args, **kwargs)

    return wrapped
