from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from marketplace.forms import SearchForm, ListingForm
from marketplace.models import Model, MarketUser, Listing, Image


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


class ListingListView(generic.ListView):
    model = Listing
    paginate_by = 5
    template_name = "marketplace/listing_list.html"
    context_object_name = "listings"

    def get_queryset(self):
        queryset = Listing.objects.all()

        brand = self.request.GET.get("brand", None)
        model = self.request.GET.get("model", None)
        year_start = self.request.GET.get("year_start", None)
        year_end = self.request.GET.get("year_end", None)
        price_start = self.request.GET.get("price_start", None)
        price_end = self.request.GET.get("price_end", None)
        mileage_start = self.request.GET.get("mileage_start", None)
        mileage_end = self.request.GET.get("mileage_end", None)

        if brand:
            queryset = queryset.filter(
                car_model__brand_id=brand
            )
        if brand:
            queryset = queryset.filter(car_model__brand=brand)
        if model:
            queryset = queryset.filter(car_model__name__icontains=model)
        if year_start:
            queryset = queryset.filter(year__gte=year_start)
        if year_end:
            queryset = queryset.filter(year__lte=year_end)
        if price_start:
            queryset = queryset.filter(price__gte=price_start)
        if price_end:
            queryset = queryset.filter(price__lte=price_end)
        if mileage_start:
            queryset = queryset.filter(mileage__gte=mileage_start)
        if mileage_end:
            queryset = queryset.filter(mileage__lte=mileage_end)

        queryset = queryset.prefetch_related(
            Prefetch(
                "images",
                queryset=Image.objects.order_by("id")[:1],
                to_attr="first_image",
            )
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_listings_count = self.get_queryset().count()
        context["num_listings"] = all_listings_count

        return context


ImageFormSet = inlineformset_factory(
    Listing,
    Image,
    fields=['image'],
    extra=1,
    can_delete=True
)


class ListingDetailView(generic.DetailView):
    model = Listing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        context['is_author'] = self.object.seller == self.request.user

        image_urls = [image.image.url for image in context['images']]
        context['image_urls'] = image_urls
        return context


class ListingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Listing
    form_class = ListingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.seller = self.request.user
        listing.save()

        context = self.get_context_data()
        image_formset = context['image_formset']

        if image_formset.is_valid():
            instances = image_formset.save(commit=False)
            for instance in instances:
                instance.listing = listing
                instance.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        user_id = self.object.seller.id
        return reverse('marketplace:sale-listings', kwargs={'pk': user_id})


class ListingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Listing
    form_class = ListingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.seller = self.request.user
        listing.save()

        context = self.get_context_data()
        image_formset = context['image_formset']

        if image_formset.is_valid():
            instances = image_formset.save(commit=False)
            for instance in image_formset.deleted_objects:
                instance.delete()
            for instance in instances:
                instance.listing = listing
                instance.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        user_id = self.object.seller.id
        return reverse_lazy('marketplace:sale-listings', kwargs={'pk': user_id})


class ListingDeleteView(LoginRequiredMixin, generic.DeleteView):
    pass


class MarketUserDetailView(LoginRequiredMixin, generic.DetailView):
    pass


class MarketUserCreateView(generic.CreateView):
    pass


class MarketUserUpdateView(LoginRequiredMixin, generic.UpdateView):
    pass


class MarketUserFavouriteListingsView(LoginRequiredMixin, generic.ListView):
    pass


class MarketUserSaleListingsView(LoginRequiredMixin, generic.ListView):
    pass


@login_required
def toggle_assign_to_listing(request, pk):
    pass
