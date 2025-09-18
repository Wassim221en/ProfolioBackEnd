from django.urls import path
from .views import create_recommendation, list_recommendations, recommendation_detail

app_name = 'recommendations'

urlpatterns = [
    # إنشاء توصية جديدة
    path('create/', create_recommendation, name='create_recommendation'),

    # عرض جميع التوصيات
    path('', list_recommendations, name='list_recommendations'),

    # عرض تفاصيل توصية محددة
    path('<uuid:pk>/', recommendation_detail, name='recommendation_detail'),
]
