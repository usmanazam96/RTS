from django.http import HttpResponse
from django.shortcuts import redirect, render


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = list(request.user.groups.values_list('name', flat=True))
                common_roles = list(set(group).intersection(allowed_roles))
                role = request.session.get('login_role', 'None')
                if role in common_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    if len(group) > 1:
                        role_switch = True

                    context = dict(page_title='403 FORBIDDEN', h1_title='403 FORBIDDEN', url='403 FORBIDDEN',
                                   role_switch=role_switch)
                    return render(request, 'RTS/error_403.html', context)

        return wrapper_func

    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_function
