from django.urls import path

from marketplace.views import (
    index, ListingCreateView, ListingListView, ListingDetailView,
    MarketUserDetailView, toggle_assign_to_listing, MarketUserCreateView,
    MarketUserUpdateView, MarketUserFavouriteListingsView, MarketUserSaleListingsView,
)


urlpatterns = [
    path("", index, name="index"),
    path(
        "listing/create/",
        ListingCreateView.as_view(),
        name="listing-create"
    ),
    path(
        "listing-detail/<int:pk>",
        ListingDetailView.as_view(),
        name="listing-detail"
    ),
    path(
        "listings-detail/<int:pk>/toggle-assign/",
        toggle_assign_to_listing,
        name="toggle-assign-to-listing",
    ),
    path("listings/", ListingListView.as_view(), name="listings-list"),
    path(
        "market-user-detail/<int:pk>/",
        MarketUserDetailView.as_view(),
        name="market-user-detail"
    ),
    path(
        "market-user/create/",
        MarketUserCreateView.as_view(),
        name="market-user-create"
    ),
    path(
        "market-user/<int:pk>/update/",
        MarketUserUpdateView.as_view(),
        name="market-user-update"
    ),
    path(
        "market-user-detail/<int:pk>/my-favourite-listings/",
        MarketUserFavouriteListingsView.as_view(),
        name="my-favourite-listings",
    ),
    path(
        "market-user-detail/<int:pk>/sale-listings/",
        MarketUserSaleListingsView.as_view(),
        name="sale-listings",
    ),
]

app_name = "marketplace"
