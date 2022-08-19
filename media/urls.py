from django.urls import include, path
from .views import MediaDownloadView, MediaListView


urlpatterns = [
    path("", MediaListView.as_view(), name="Media List View"),
    path("download", MediaDownloadView.as_view(), name="Media Download View"),
]
