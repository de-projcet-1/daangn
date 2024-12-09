from django.urls import path, include

urlpatterns = [
    path('item/', include('category.urls')),
]
