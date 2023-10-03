from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import generic

from marketplace.forms import SearchForm
from marketplace.models import Model, MarketUser, Listing


def index(request: HttpRequest):

    form = SearchForm(request.GET)
    context = {
        "num_listings": Listing.objects.count(),
        "num_users": MarketUser.objects.count(),
        "num_models": Model.objects.count()
    }

    if form.is_valid():
        context.update({'search_form': form, })
        return render(request, "marketplace/index.html", context=context)


class ListingCreateView(LoginRequiredMixin, generic.CreateView):
    pass


class ListingListView(generic.ListView):
    pass
