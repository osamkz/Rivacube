from django.urls import include, path
from .views import MediaListView


urlpatterns = [
    path("", MediaListView.as_view(), name="Media List View"),
]
