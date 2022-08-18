from django.shortcuts import render

from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Media

# Create your views here.


class MediaListView(LoginRequiredMixin, ListView):
    # TODO: Ajouter les options de filtre et de tri
    def get_queryset(self):
        return Media.objects.all()

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
        context["current_limit"] = self.request.GET.get("limit")

        return context

    model = Media
    template_name = "media/index.html"
    paginate_by = 100

# TODO: Creer la classe de Download
# TODO: Creer la class API
