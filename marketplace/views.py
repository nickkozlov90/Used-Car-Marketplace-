from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Prefetch
from django.forms import inlineformset_factory
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic, View

from marketplace.forms import (
    SearchForm,
    ListingForm,
    MarketUserCreationForm,
    MarketUserUpdateForm,
    UserPasswordChangeForm,
)
from marketplace.models import Model, MarketUser, Listing, Image


def index(request: HttpRequest):
    form = SearchForm(request.GET)
    context = {
        "num_listings": Listing.objects.count(),
        "num_users": MarketUser.objects.count(),
        "num_models": Model.objects.count(),
    }

    if form.is_valid():
        context.update(
            {
                "search_form": form,
            }
        )
        return render(request, "marketplace/index.html", context=context)


class ListingListView(generic.ListView):
    model = Listing
    paginate_by = 5
    template_name = "marketplace/listing_list.html"
    context_object_name = "listings"

    def get_queryset(self):
        queryset = Listing.objects.all()

        brand = self.request.GET.get("brand")
        model = self.request.GET.get("model")
        year_start = self.request.GET.get("year_start")
        year_end = self.request.GET.get("year_end")
        price_start = self.request.GET.get("price_start")
        price_end = self.request.GET.get("price_end")
        mileage_start = self.request.GET.get("mileage_start")
        mileage_end = self.request.GET.get("mileage_end")

        if brand:
            queryset = queryset.filter(car_model__brand__id=brand)
        if model:
            queryset = queryset.filter(car_model__id=model)
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
    Listing, Image, fields=["image"], extra=1, can_delete=True
)


class ListingDetailView(generic.DetailView):
    model = Listing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = self.object.images.all()
        context["is_author"] = self.object.seller == self.request.user

        return context


class ListingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Listing
    form_class = ListingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["image_formset"] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.seller = self.request.user
        listing.save()

        context = self.get_context_data()
        image_formset = context["image_formset"]

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
        return reverse("marketplace:sale-listings", kwargs={"pk": user_id})


class ListingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Listing
    form_class = ListingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["image_formset"] = ImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["image_formset"] = ImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        listing = form.save(commit=False)
        listing.seller = self.request.user
        listing.save()

        context = self.get_context_data()
        image_formset = context["image_formset"]

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
        return reverse_lazy(
            "marketplace:sale-listings",
            kwargs={"pk": user_id},
        )


class ListingDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Listing

    def get_success_url(self):
        user_id = self.object.seller.id
        return reverse("marketplace:sale-listings", kwargs={"pk": user_id})


class MarketUserDetailView(LoginRequiredMixin, generic.DetailView):
    model = MarketUser
    template_name = "marketplace/market_user_detail.html"

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        queryset = MarketUser.objects.filter(id=user_id)

        return queryset


class MarketUserCreateView(generic.CreateView):
    model = MarketUser
    form_class = MarketUserCreationForm

    def get_success_url(self):
        return reverse(
            "marketplace:market-user-detail",
            kwargs={"pk": self.object.pk},
        )


class MarketUserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = MarketUser
    form_class = MarketUserUpdateForm

    def get_success_url(self):
        return reverse_lazy(
            "marketplace:market-user-detail",
            kwargs={"pk": self.object.pk},
        )


class MarketUserFavouriteListingsView(LoginRequiredMixin, generic.ListView):
    model = Listing
    template_name = "marketplace/listing_list.html"
    paginate_by = 5
    context_object_name = "listings"

    def get_queryset(self):
        user_id = self.kwargs.get("pk")
        if self.request.user.id != user_id:
            return Listing.objects.none()

        queryset = Listing.objects.filter(users__in=[self.request.user])

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


class MarketUserSaleListingsView(LoginRequiredMixin, generic.ListView):
    model = Listing
    paginate_by = 5
    template_name = "marketplace/listing_list.html"
    context_object_name = "listings"

    def get_queryset(self):
        user_id = self.kwargs.get("pk")

        queryset = Listing.objects.filter(seller_id=user_id)
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


class ToggleAssignToListingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = MarketUser.objects.get(id=request.user.id)
        listing = get_object_or_404(Listing, id=pk)

        if listing in user.favourite_listings.all():
            user.favourite_listings.remove(listing)
        else:
            user.favourite_listings.add(listing)

        return HttpResponseRedirect(
            reverse_lazy("marketplace:listing-detail", args=[pk])
        )


class UserPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change.html"
    form_class = UserPasswordChangeForm
