from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render
from .models import Ticker
from rest_framework import generics
from .serializers import TickerSerializer
from django.shortcuts import render

from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin


class TickerList(generics.ListAPIView):
    # Also used for TickerListView, TickerMarketList
    def get_queryset(self):
        # Sort & Order
        o = "-" if self.request.GET.get("order") == "desc" else ""
        if self.request.GET.get("sort"):
            data = Ticker.objects.order_by(
                o + self.request.GET.get("sort")).all()
        else:
            data = Ticker.objects.order_by("-date").all()

        # Ticker
        if self.request.GET.get("ticker"):
            data = data.filter(yticker=self.request.GET.get("ticker"))

        # Date
        if self.request.GET.get("startDate") and self.request.GET.get("endDate"):
            data = data.filter(date__range=[self.request.GET.get(
                "startDate"), self.request.GET.get("endDate")])
        elif self.request.GET.get("startDate"):
            data = data.filter(date__range=[self.request.GET.get(
                "startDate"), date.today()])

        # Market
        if self.request.GET.get("market"):
            data = data.filter(yticker__market=self.request.GET.get("market"))

        # Limit
        if (self.request.get_full_path().split("?")[0] == "/api" and self.request.GET.get("limit")):
            return data[:int(self.request.GET.get("limit"))]
        if (self.request.get_full_path().split("?")[0] == "/api"):
            return data
        if (len(self.request.GET)) == 0:
            return data[:10000]
        if self.request.GET.get("limit"):
            return data[:int(self.request.GET.get("limit"))]
        return data[:1000000]

    serializer_class = TickerSerializer


class TickerReactView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {})


class TickerListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return TickerList.get_queryset(self)

    def get_tickers(self):
        return list(map(lambda x: x[0], (list(Ticker.objects.order_by(
            "yticker").values_list('yticker').distinct()))))

    def get_markets(self):
        return list(map(lambda x: x[0], (list(Ticker.objects.order_by(
            "yticker__market").values_list('yticker__market').distinct()))))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recupere la liste de tickers
        tickers = self.get_tickers()

        # Recupere la liste des marchés
        markets = self.get_markets()

        context["tickers"] = tickers
        context["markets"] = markets
        context["count"] = len(self.get_queryset())
        context["current_ticker"] = self.request.GET.get("ticker") or ""
        context["current_start_date"] = self.request.GET.get("startDate") or ""
        context["current_end_date"] = self.request.GET.get("endDate") or ""
        context["current_sort"] = self.request.GET.get("sort") or ""
        context["current_order"] = self.request.GET.get("order") or ""
        context["current_limit"] = self.request.GET.get("limit") or "1000000"
        context["current_market"] = self.request.GET.get("market") or ""

        return context

    model = Ticker
    template_name = "ticker/index.html"
    paginate_by = 100


class TickerDownloadView(TickerListView):
    template_name: str = "ticker/sample.csv"
    content_type: str = "text/csv"
    paginate_by: int = 1000000


# TODO: A Finir
class TickerMarketList(generics.ListAPIView):
    # TODO: Ajouter le bon market depuis le body (ou les parametres) de la requete
    # TODO: Ajouter le path dans urls.py
    def get_queryset(self):
        return TickerList().get_queryset().filter(yticker__market=None)
