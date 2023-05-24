from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def user_tested (fonc_test=None, view_return=None):
    def decorator(actual_view):
        @wraps(actual_view)
        def _wrapper_view (request, *args, **kwargs):
            if not fonc_test(request.user):
                return actual_view(request, *args, **kwargs)
            return redirect(view_return)
        
        return _wrapper_view
    
    return decorator


def if_user_authentificated(view_return):
    
    def user_auth (user):
        if user.is_authenticated:
            return True
        return False
    
    return user_tested(user_auth, view_return)


def drh_required (url_return=None, raise_exception=False):
    
    def check_role (user):
        if user.role == 'DRH':
            return True
        
        if raise_exception:
            raise PermissionDenied
        
        return False

    return user_passes_test(check_role, login_url=url_return)


def employe_deni (url_return=None, raise_exception=False):
    
    def check_role (user):
        if user.role != 'EMPLOYE':
            return True
        
        if raise_exception:
            raise PermissionDenied
        
        return False

    return user_passes_test(check_role, login_url=url_return)