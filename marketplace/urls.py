from django.urls import path

from marketplace.views import index, ListingCreateView, ListingListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "listing/create/",
        ListingCreateView.as_view(),
        name="listing-create"
    ),
    path("listings/", ListingListView.as_view(), name="listings-list"),
]

app_name = "marketplace"
