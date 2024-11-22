from django.urls import path
from .views import travel_recommendations, travel_detail

urlpatterns = [
    path('', travel_recommendations, name='travel_recommendations'),
    path('<int:id>/', travel_detail, name='travel_detail'),
]
