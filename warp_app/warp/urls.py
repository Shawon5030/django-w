from django.urls import path
from .views import WarpView

urlpatterns = [
    path('', WarpView.as_view(), name='warp'),
]
