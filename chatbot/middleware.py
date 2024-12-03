from django.utils.timezone import now
from datetime import timedelta
from .models import ChatSession
import time

class ExpiredSessionMiddleware:
    last_cleanup = 0  # 마지막 정리 시간 

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 현재 시간 (초 단위)
        current_time = time.time()
        
        # 10분마다 한 번만 정리
        if current_time - self.last_cleanup > 600:
            expiration_time = now() - timedelta(minutes=10)
            deleted_count = ChatSession.objects.filter(created_at__lt=expiration_time).delete()[0]
            self.last_cleanup = current_time
            
            # 디버그 출력
            if deleted_count > 0:
                print(f"[Middleware] Deleted {deleted_count} expired sessions.")

        response = self.get_response(request)
        return response
