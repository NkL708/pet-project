from django.urls import path

from ..views.users import UserListView

urlpatterns = [path("", UserListView.as_view())]
