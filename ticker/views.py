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
    def get_queryset(self):
        o = "-" if self.request.GET.get("desc") == "-" else ""
        if self.request.GET.get("sort"):
            data = Ticker.objects.order_by(
                o + self.request.GET.get("sort")).all()
        else:
            data = Ticker.objects.order_by("-date").all()
        if self.request.GET.get("ticker"):
            data = data.filter(yticker=self.request.GET.get("ticker"))
        if self.request.GET.get("startDate") and self.request.GET.get("endDate"):
            data = data.filter(date__range=[self.request.GET.get(
                "startDate"), self.request.GET.get("endDate")])
        elif self.request.GET.get("startDate"):
            data = data.filter(date__range=[self.request.GET.get(
                "startDate"), date.today()])

        return data[:1000000]

    serializer_class = TickerSerializer


class TickerReactView(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {})


class TickerListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        o = "-" if self.request.GET.get("desc") == "-" else ""
        if self.request.GET.get("sort"):
            data = Ticker.objects.order_by(
                o + self.request.GET.get("sort")).all()
        else:
            data = Ticker.objects.order_by("-date").all()
        if self.request.GET.get("ticker"):
            data = data.filter(yticker=self.request.GET.get("ticker"))
        if self.request.GET.get("startDate") and self.request.GET.get("endDate"):
            data = data.filter(date__range=[self.request.GET.get(
                "startDate"), self.request.GET.get("endDate")])
        elif self.request.GET.get("startDate"):
            data = data.filter(date__range=[self.request.GET.get(
                "startDate"), date.today()])

        if (len(self.request.GET)) == 0:
            return data[:10000]
        if self.request.GET.get("limit"):
            return data[:int(self.request.GET.get("limit"))]
        return data[:1000000]

    def get_tickers(self):
        return list(map(lambda x: x[0], (list(Ticker.objects.order_by(
            "yticker").values_list('yticker').distinct()))))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recupere la liste de tickers
        tickers = self.get_tickers()

        context["tickers"] = tickers
        context["count"] = len(self.get_queryset())
        context["current_ticker"] = self.request.GET.get("ticker") or ""
        context["current_start_date"] = self.request.GET.get("startDate") or ""
        context["current_end_date"] = self.request.GET.get("endDate") or ""
        context["current_sort"] = self.request.GET.get("sort") or ""
        context["current_order"] = self.request.GET.get("desc") or ""
        context["current_limit"] = self.request.GET.get("limit") or "1000000"

        return context

    model = Ticker
    template_name = "ticker/index.html"
    paginate_by = 100


class TickerDownloadView(TickerListView):
    template_name: str = "ticker/sample.csv"
    content_type: str = "text/csv"
    paginate_by: int = 1000000
