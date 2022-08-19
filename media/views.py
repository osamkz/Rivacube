from django.shortcuts import render

from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Media

from datetime import date

# Create your views here.


class MediaListView(LoginRequiredMixin, ListView):
    def get_queryset(self):

        # Sort & Order
        o = "-" if self.request.GET.get("order") == "desc" else ""
        if self.request.GET.get("sort") and self.request.GET.get("sort") != "None":
            media = Media.objects.order_by(
                o + self.request.GET.get("sort")).all()
        else:
            media = Media.objects.order_by("-created_at").all()

        # Htag
        if self.request.GET.get("htag") and self.request.GET.get("htag") != "None":
            media = media.filter(htag=self.request.GET.get("htag"))

        # Source
        if self.request.GET.get("source") and self.request.GET.get("source") != "None":
            media = media.filter(source=self.request.GET.get("source"))

        # Date
        if self.request.GET.get("startDate") and self.request.GET.get("endDate") and self.request.GET.get("startDate") != "None" and self.request.GET.get("endDate") != "None":
            media = media.filter(created_at__range=[self.request.GET.get(
                "startDate"), self.request.GET.get("endDate")])
        elif self.request.GET.get("startDate") and self.request.GET.get("startDate") != "None":
            media = media.filter(created_at__range=[self.request.GET.get(
                "startDate"), date.today()])

        # Quote
        if self.request.GET.get("quote") and self.request.GET.get("quote") != "None":
            media = media.filter(is_quote=self.request.GET.get("quote"))

        # Retweet
        if self.request.GET.get("retweet") and self.request.GET.get("retweet") != "None":
            media = media.filter(is_retweet=self.request.GET.get("retweet"))

        # Langue
        if self.request.GET.get("lang") and self.request.GET.get("lang") != "None":
            media = media.filter(lang=self.request.GET.get("lang"))

        # Limite
        if self.request.GET.get("limit") and self.request.GET.get("limit") != "None":
            media = media[:int(self.request.GET.get("limit"))]
        else:
            media = media[:10000]

        return media

    def get_htag(self):
        return list(map(lambda x: x[0], (list(Media.objects.order_by(
            "htag").values_list('htag').distinct()))))

    def get_source(self):
        return list(map(lambda x: x[0], (list(Media.objects.order_by(
            "source").values_list('source').distinct()))))

    def get_lang(self):
        return list(map(lambda x: x[0], (list(Media.objects.order_by(
            "lang").values_list('lang').distinct()))))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["count"] = len(self.get_queryset())

        context["htags"] = self.get_htag()
        context["current_htag"] = self.request.GET.get("htag")
        context["sources"] = self.get_source()
        context["current_source"] = self.request.GET.get("source")
        context["langs"] = self.get_lang()
        context["current_lang"] = self.request.GET.get("lang")
        context["current_start_date"] = self.request.GET.get("startDate")
        context["current_end_date"] = self.request.GET.get("endDate")
        context["current_quote"] = self.request.GET.get("quote")
        context["current_retweet"] = self.request.GET.get("retweet")
        context["current_lang"] = self.request.GET.get("lang")
        context["current_sort"] = self.request.GET.get("sort")
        context["current_order"] = self.request.GET.get("order")
        context["current_limit"] = self.request.GET.get("limit") or 10000

        return context

    model = Media
    template_name = "media/index.html"
    paginate_by = 100


class MediaDownloadView(MediaListView):
    template_name: str = "media/sample.csv"
    content_type: str = "text/csv"
    paginate_by: int = 1000000

# TODO: Creer la class API
