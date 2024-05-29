from django.urls import path, include
from . import views


urlpatterns = [
    path("new_service/", views.new_service, name="new_service"),
    path("list_services/", views.list_services, name="list_services"),
    path("update_list/", views.update_list, name="update_list")
]
