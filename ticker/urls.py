from django.urls import include, path
from .views import TickerDownloadView, TickerList, TickerListView, TickerMarketList


urlpatterns = [
    path('api', TickerList.as_view(), name="Tiker List"),
    path("", TickerListView.as_view(), name="Ticker List View"),
    path("download", TickerDownloadView.as_view(), name="Ticker Download View"),
    path("api/market/<str:market>",
         TickerMarketList.as_view(), name="Ticker Market List")
]
