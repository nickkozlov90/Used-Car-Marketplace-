from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from marketplace.models import (
    Brand, Model, Listing, Image, MarketUser
)


@admin.register(Brand)
class CarBrandAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Model)
class CarModelAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Listing)
class CarListingAdmin(admin.ModelAdmin):
    list_display = [
        "car_model",
        "year",
        "price",
        "mileage",
        "created_at"
    ]
    search_fields = ["car_model__name", "seller__username", "created_at"]
    list_filter = [
        "car_model__name",
        "created_at",
        "year",
        "price",
        "mileage"
    ]


@admin.register(MarketUser)
class MarketUserAdmin(UserAdmin):
    list_display = (*UserAdmin.list_display, "phone_number")
    fieldsets = (*UserAdmin.fieldsets, (
        "Additional info", {"fields": ("favourite_listings",)}
    )
    )


admin.site.register(Image)
