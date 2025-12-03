from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from core.decorators import auth_required
from psql import psqlManager
import json

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        manager = psqlManager.Manager(__name__)
        profile_user = manager.getProfile(email=email)
        
        if not profile_user:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)
        
        if profile_user.status.lower() != 'active':
            return JsonResponse({'error': 'Account is not active'}, status=400)
        
        if profile_user.password != password:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)
        
        role_obj = manager.getRole(role_id=profile_user.role_id)
        is_admin = role_obj.name.lower() == 'admin' if role_obj else False
        
        request.session['user_email'] = profile_user.email
        request.session['is_admin'] = is_admin
        
        user_data = {
            'id': profile_user.id,
            'email': profile_user.email,
            'firstname': profile_user.firstname,
            'lastname': profile_user.lastname,
            'signup_type': profile_user.signup_type,
            'isAdmin': is_admin
        }
        return JsonResponse({'message': 'Login successful', 'user': user_data, 'success': True}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        firstname = data.get('firstname', '').strip()
        lastname = data.get('lastname', '').strip()
        
        manager = psqlManager.Manager(__name__)
        
        registration_user = manager.getRegistration(email=email)
        if registration_user:
            return JsonResponse({'error': 'Email already registered'}, status=400)
        
        new_registration_user = manager.createRegistration(email, firstname, lastname, "inactive", "custom")
        
        user_data = {
            'email': email,
            'firstname': firstname,
            'lastname': lastname
        }
        return JsonResponse({'message': 'Registration successful', 'user': user_data}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def set_password(request, unique_identifier):
    try:
        data = json.loads(request.body)
        new_password = data.get('new_password') or data.get('password')
        
        manager = psqlManager.Manager(__name__)
        profile_user = manager.getProfile(unique_identifier=unique_identifier)
        
        if not profile_user:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        profile_user.password = new_password
        profile_user.status = 'active'
        manager.update(profile_user)
        
        return JsonResponse({'message': 'Password set successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def forgot_password(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').lower().strip()
        
        manager = psqlManager.Manager(__name__)
        profile_user = manager.getProfile(email=email)
        
        return JsonResponse({
            'message': 'If an account exists with this email, you will receive password reset instructions.'
        }, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    try:
        request.session.flush()
        
        response = JsonResponse({'message': 'Logged out successfully'}, status=200)
        response.delete_cookie('sessionid')
        
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@auth_required
@require_http_methods(["GET"])
def profile_view(request):
    try:
        manager = request.db_manager
        profile_user = manager.getProfile(email=request.user_email)
        
        if not profile_user:
            return JsonResponse({'error': 'Profile not found'}, status=404)
        
        role_obj = manager.getRole(role_id=profile_user.role_id)
        is_admin = role_obj.name.lower() == 'admin' if role_obj else False
        
        user_data = {
            'email': profile_user.email,
            'firstname': profile_user.firstname,
            'lastname': profile_user.lastname,
            'isAdmin': is_admin
        }
        return JsonResponse({'profile': user_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@auth_required
@csrf_exempt
@require_http_methods(["POST"])
def update_profile(request):
    try:
        data = json.loads(request.body)
        
        manager = request.db_manager
        profile_user = manager.getProfile(email=request.user_email)
        profile_user.firstname = data.get('firstname', profile_user.firstname)
        profile_user.lastname = data.get('lastname', profile_user.lastname)
        manager.update(profile_user)
        
        return JsonResponse({'message': 'Profile updated successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@auth_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_account(request):
    try:
        manager = request.db_manager
        profile_user = manager.getProfile(email=request.user_email)
        profile_user.status = 'deleted'
        manager.update(profile_user)
        
        request.session.flush()
        return JsonResponse({'message': 'Account deleted successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def check_auth(request):
    try:
        email = request.session.get('user_email')
        if not email:
            return JsonResponse({'isAuthenticated': False}, status=200)
        
        manager = psqlManager.Manager(__name__)
        profile_user = manager.getProfile(email=email)
        
        if not profile_user:
            request.session.flush()
            return JsonResponse({'isAuthenticated': False}, status=200)
        
        role_obj = manager.getRole(role_id=profile_user.role_id)
        is_admin = role_obj.name.lower() == 'admin' if role_obj else False
        
        user_data = {
            'email': profile_user.email,
            'firstname': profile_user.firstname,
            'lastname': profile_user.lastname,
            'isAdmin': is_admin
        }
        return JsonResponse({'isAuthenticated': True, 'user': user_data}, status=200)
    except Exception as e:
        return JsonResponse({'isAuthenticated': False}, status=200)
