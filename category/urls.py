from django.urls import path
from . import views

urlpatterns = [
    path('region/', views.get_region, name='region'),
    path('keyword/', views.get_keywords_by_region, name='keyword'),
    path('generate-wordcloud/<int:region_id>/', views.generate_wordcloud, name='generate_wordcloud'),
]
