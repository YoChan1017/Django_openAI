from django.urls import path
from .views import plan

urlpatterns = [
    path('', plan, name='calendar'),  # 기본 일정 생성
    path('<int:place_id>/', plan, name='calendar_place'),  # 특정 장소 조회
]
