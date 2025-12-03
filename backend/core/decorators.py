from functools import wraps
from django.http import JsonResponse


def auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        email = request.session.get('user_email')
        if email:
            from psql import psqlManager
            request.db_manager = psqlManager.Manager(__name__)
            request.user_email = email
            
            return view_func(request, *args, **kwargs)
        return JsonResponse({'error': 'Authentication required'}, status=401)
    return _wrapped_view


def admin_group_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        email = request.session.get('user_email')
        if not email:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        is_admin = request.session.get('is_admin', False)
        if not is_admin:
            return JsonResponse({'error': 'You must be an admin to perform this action'}, status=403)
        
        from psql import psqlManager
        request.db_manager = psqlManager.Manager(__name__)
        request.user_email = email
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
