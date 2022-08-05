from django.urls import include, path
from .views import TickerList, TickerListView


urlpatterns = [
    path('api', TickerList.as_view(), name="ticker-list"),
    path("", TickerListView.as_view(), name="Ticker List View")
]
