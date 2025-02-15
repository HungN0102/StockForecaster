from .models import HotTopic

def global_context(request):
    latest_hottopic = HotTopic.objects.order_by('-created_at').first()
    latest_hottopics = HotTopic.objects.filter(group_id=latest_hottopic.group_id)
    return {
        "latest_hottopics": latest_hottopics
    }