from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .models import UserSubscription

def require_feature(feature_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Get user's active subscription
            subscription = UserSubscription.objects.filter(
                user=request.user,
                status='active'
            ).first()
            
            if not subscription or not subscription.has_feature(feature_name):
                return Response(
                    {
                        "error": "This feature requires a subscription",
                        "feature": feature_name,
                        "required_plan": subscription.plan.name if subscription else None
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator 