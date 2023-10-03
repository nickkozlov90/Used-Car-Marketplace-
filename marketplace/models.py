from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Model(models.Model):
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name="models",
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.brand.name} {self.name}"


class Listing(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="car_listings",
    )
    car_model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="car_models")
    year = models.IntegerField()
    price = models.IntegerField()
    mileage = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def first_photo(self) -> object:
        return self.images.first()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.car_model.name}, {self.price}, {self.created_at.strftime('%d %b %Y')}"


class Image(models.Model):
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(null=True)

    def image_upload_to(self, filename):
        return f'images/listing_{self.listing.id}/{filename}'

    image.upload_to = image_upload_to


class MarketUser(AbstractUser):
    profile_picture = models.ImageField(null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True)
    favourite_listings = models.ManyToManyField(
        Listing,
        related_name="users",
        blank=True
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.first_name

    def image_upload_to(self, filename):
        return f'images/marketuser_{self.id}/{filename}'

    profile_picture.upload_to = image_upload_to
