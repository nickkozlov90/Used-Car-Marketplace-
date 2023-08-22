from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class CarBrand(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(
        CarBrand,
        on_delete=models.CASCADE,
        related_name="models",
    )
    name = models.CharField(max_length=255)


class CarListing(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="car_listings",
    ),
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE,)
    year = models.DecimalField(max_digits=4)
    price = models.DecimalField(max_digits=4)
    mileage = models.DecimalField(max_digits=4)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.car_model.brand.name} {self.car_model.name}, " \
               f"{self.price}, {self.created_at}"


class CarImage(models.Model):
    listing = models.ForeignKey(
        CarListing,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField()


class User(AbstractUser):
    profile_picture = models.ImageField()
    favourite_listings = models.ManyToManyField(
        CarListing,
        related_name="users",
    )

    class Meta:
        ordering = ["username"]
