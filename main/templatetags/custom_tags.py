# Custom template tags for notification:
from django import template
from main.models import Notification

register = template.Library()


@register.inclusion_tag('main/show_notifications.html', takes_context=True)
# passing 'context' as parameter
def show_notifications(context):
    # to get our current user has logged-in for the specific user notification.
    request_user = context['request'].user
    # 'to_user' is the one who is receiving the notifications.
    notifications = Notification.objects.filter(
        to_user=request_user).exclude(user_has_seen=True).order_by('-date')
    return {'notifications': notifications}
