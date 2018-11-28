from django.core.exceptions import PermissionDenied


def user_is_user(function):
    """Decorador que verifica que el usuario es de tipo Usuario"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'user'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap


def user_is_breeder(function):
    """Decorador que verifica que el usuario es de tipo Breeder"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'breeder'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap


def user_is_association(function):
    """Decorador que verifica que el usuario es de tipo Association"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'association'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap


def user_is_administrator(function):
    """Decorador que verifica que el usuario es de tipo Administrador (y staff)"""

    def wrap(request, *args, **kwargs):
        if hasattr(request.user.actor, 'administrator') and (request.user.is_staff):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
