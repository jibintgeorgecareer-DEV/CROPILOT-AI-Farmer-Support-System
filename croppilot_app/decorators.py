from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user_role = request.user.profile.role

            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/login/')
        return wrapper
    return decorator
