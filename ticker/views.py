from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.list import ListView
from django.shortcuts import render
from .models import Ticker
from rest_framework import generics
from .serializers import TickerSerializer
from django.shortcuts import render

from datetime import date


# Afficher les elements
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


class TickerListView(ListView):
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

    def get_tickers(self):
        return list(map(lambda x: x[0], (list(Ticker.objects.order_by(
            "yticker").values_list('yticker').distinct()))))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recupere la liste de tickers
        tickers = self.get_tickers()

        context["tickers"] = tickers
        context["count"] = len(self.get_queryset())
        context["current_ticker"] = self.request.GET.get("ticker")
        context["current_start_date"] = self.request.GET.get("startDate")
        context["current_end_date"] = self.request.GET.get("endDate")
        context["current_sort"] = self.request.GET.get("sort")
        context["current_order"] = self.request.GET.get("desc")

        return context

    model = Ticker
    template_name = "index.html"
    paginate_by = 100


class TickerDownloadView(TickerListView):
    template_name: str = "sample.csv"
    content_type: str = "text/csv"
    paginate_by: int = 1000000


class toRemoveMaybe(View):
    def get(self, request):
        o = "-" if request.GET.get("desc") == "-" else ""
        if request.GET.get("sort"):
            data = Ticker.objects.order_by(
                o + request.GET.get("sort")).all()
        else:
            data = Ticker.objects.order_by("-date").all()
        if request.GET.get("ticker"):
            data = data.filter(yticker=request.GET.get("ticker"))
        if request.GET.get("startDate") and request.GET.get("endDate"):
            data = data.filter(date__range=[request.GET.get(
                "startDate"), request.GET.get("endDate")])
        elif request.GET.get("startDate"):
            data = data.filter(date__range=[request.GET.get(
                "startDate"), date.today()])

        data = data[0]

        print(repr(data))

        self.file_name = "Tickers.xlsx"
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="Tickers.csv"'},
        )
        return response
