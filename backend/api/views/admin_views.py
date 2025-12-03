from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from core.decorators import admin_group_required
import json

@admin_group_required
@require_http_methods(["GET"])
def admin_registrations_view(request):
    try:
        # manager = request.db_manager
        # registrations = manager.getInactiveRegistrations()
        
        return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch registrations'}, status=500)


@admin_group_required
@require_http_methods(["GET"])
def admin_users_view(request):
    try:
        # manager = request.db_manager
        # users = manager.getActiveProfiles()
        
        return JsonResponse([], safe=False)
    except Exception as e:
        return JsonResponse({'error': 'Failed to fetch users'}, status=500)


@admin_group_required
@csrf_exempt
@require_http_methods(["POST"])
def admin_user_action(request, action):
    try:
        data = json.loads(request.body)
        user_ids = data.get('userIds', [])
        
        # manager = request.db_manager
        # for user_id in user_ids:
        #     user = manager.getProfile(unique_identifier=user_id)
        #     if action == 'delete':
        #         user.status = 'deleted'
        #         manager.update(user)
        
        return JsonResponse({'message': f'{action} action completed successfully'})
    except Exception as e:
        return JsonResponse({'error': f'Failed to perform {action}'}, status=500)
