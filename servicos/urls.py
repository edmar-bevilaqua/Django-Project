from django.urls import path, include
from . import views


urlpatterns = [
    path("new_service/", views.new_service, name="new_service"),
]
