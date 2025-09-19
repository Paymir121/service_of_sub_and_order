from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed

from subscriptions.models import UserSubscription

from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication

User = get_user_model()

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.token_auth = TokenAuthentication()

    def __call__(self, request):
        path = request.path_info
        print('MW.1: ', path.startswith('/api/products/'))
        if not path.startswith('/api/products/'):
            return self.get_response(request)
        print('MW.2: ', path.startswith('/api/products/'))

        try:
            auth_result = self.token_auth.authenticate(request)
            if auth_result is not None:
                user, token = auth_result
                request.user = user
                request.auth = token
        except AuthenticationFailed:
            return JsonResponse(
                {
                    'error': 'I dont know who you',
                    'message': 'I dont know who you'
                },
                status=404
            )
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    'error': 'I dont know who you',
                    'message': 'I dont know who you'
                },
                status=404
            )
        print('MW.3: ', request.user.is_authenticated)
        try:
            active_subscription = UserSubscription.objects.get(
                follower=request.user,
                is_active=True
            )
            print('MW.4: ', active_subscription)
            return self.get_response(request)

        except ObjectDoesNotExist:
            return JsonResponse(
                {
                    'error': 'No active subscription',
                    'message': 'Please subscribe to access this content'
                },
                status=403
            )

        except Exception as e:
            return JsonResponse(
                {
                    'error': 'Error checking subscription',
                    'message': str(e)
                },
                status=500
            )