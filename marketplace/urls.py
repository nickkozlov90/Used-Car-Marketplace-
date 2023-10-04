from django.urls import path

from marketplace.views import (
    index, ListingCreateView, ListingListView, ListingDetailView,
    MarketUserDetailView, toggle_assign_to_listing, MarketUserCreateView,
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
]

app_name = "marketplace"
