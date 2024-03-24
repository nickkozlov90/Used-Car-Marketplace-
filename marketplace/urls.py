from django.urls import path

from marketplace.views import (
    index,
    ListingCreateView,
    ListingListView,
    ListingDetailView,
    MarketUserDetailView,
    ToggleAssignToListingView,
    MarketUserCreateView,
    MarketUserUpdateView,
    MarketUserFavouriteListingsView,
    MarketUserSaleListingsView,
    ListingUpdateView,
    ListingDeleteView,
    UserPasswordChangeView,
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
        "listing/<int:pk>/update/",
        ListingUpdateView.as_view(),
        name="listing-update"
    ),
    path(
        "listing/<int:pk>/delete/",
        ListingDeleteView.as_view(),
        name="listing-delete"
    ),
    path(
        "listings-detail/<int:pk>/toggle-assign/",
        ToggleAssignToListingView.as_view(),
        name="toggle-assign-to-listing",
    ),
    path(
        "listings/",
        ListingListView.as_view(),
        name="listings-list"
    ),
    path(
        "market-user-detail/<int:pk>/",
        MarketUserDetailView.as_view(),
        name="market-user-detail",
    ),
    path(
        "market-user/create/",
        MarketUserCreateView.as_view(),
        name="market-user-create",
    ),
    path(
        "market-user/<int:pk>/update/",
        MarketUserUpdateView.as_view(),
        name="market-user-update",
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
    path(
        "accounts/password_change/",
        UserPasswordChangeView.as_view(),
        name="password_change",
    ),
]

app_name = "marketplace"
