import os

from django.contrib.auth import get_user_model
from django.test import TestCase

from marketplace.models import Brand, Model, Listing, MarketUser, Image


class ModelsTests(TestCase):
    def test_brand_str(self):
        manufacturer = Brand.objects.create(name="test")
        self.assertEqual(str(manufacturer), f"{manufacturer.name}")

    def test_model_str(self):
        brand = Brand.objects.create(name="test_brand_name")
        model = Model.objects.create(brand=brand, name="test_model_name")
        self.assertEqual(str(model), f"{brand.name} {model.name}")

    def test_market_user_str(self):
        user = get_user_model().objects.create_user(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test$23456789",
            phone_number="+380961234576",
            profile_picture=None,
        )

        self.assertEqual(str(user), f"{user.first_name}")

    def test_listing_str(self):
        seller = MarketUser.objects.create(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test$23456789",
            phone_number="+380961234576",
            profile_picture=None,
        )
        brand = Brand.objects.create(name="test_brand")
        model = Model.objects.create(brand=brand, name="test_model")
        listing = Listing.objects.create(
            seller=seller,
            car_model=model,
            year=2020,
            price=15000,
            mileage=50000,
            description="test_description",
        )
        self.assertEqual(
            str(listing),
            f"{listing.car_model.name}, {listing.price},"
            f" {listing.created_at.strftime('%d %b %Y')}",
        )

    def test_listing_image_upload_to(self):
        seller = MarketUser.objects.create(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test$23456789",
            phone_number="+380961234580",
            profile_picture=None,
        )
        brand = Brand.objects.create(name="test_brand")
        model = Model.objects.create(brand=brand, name="test_model")
        listing = Listing.objects.create(
            seller=seller,
            car_model=model,
            year=2020,
            price=15000,
            mileage=50000,
            description="test_description",
        )
        image = Image(listing=listing)
        file_path = image.image_upload_to("example.jpg")
        self.assertEqual(
            file_path,
            os.path.join("images", f"listing_{listing.id}", "example.jpg")
        )

    def test_user_profile_image_upload_to(self):
        user = MarketUser.objects.create(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test$23456789",
            phone_number="+380961231111",
            profile_picture=None,
        )
        file_path = user.image_upload_to("profile.jpg")
        self.assertEqual(
            file_path,
            os.path.join("images", f"marketuser_{user.id}", "profile.jpg")
        )

    def test_market_user_listing_relationship(self):
        user = MarketUser.objects.create(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test$23456789",
            phone_number="+380967777777",
            profile_picture=None,
        )
        user.save()
        brand = Brand.objects.create(name="test_brand")
        model_1 = Model.objects.create(brand=brand, name="test_model_1")
        model_2 = Model.objects.create(brand=brand, name="test_model_2")

        seller_1 = MarketUser.objects.create(
            first_name="test_first_seller_name_1",
            last_name="test_last_seller_name_1",
            username="test_seller_username_1",
            password="test$23456789",
            phone_number="+380963333333",
            profile_picture=None,
        )
        seller_2 = MarketUser.objects.create(
            first_name="test_first_seller_name_2",
            last_name="test_last_seller_name_2",
            username="test_seller_username_2",
            password="test$23456789",
            phone_number="+380961111111",
            profile_picture=None,
        )

        listing_1 = Listing.objects.create(
            seller=seller_1,
            car_model=model_1,
            year=2020,
            price=15000,
            mileage=50000,
            description="test_description_1",
        )

        listing_2 = Listing.objects.create(
            seller=seller_2,
            car_model=model_2,
            year=2000,
            price=20000,
            mileage=30000,
            description="test_description_2",
        )

        user.favourite_listings.add(listing_1)
        user.favourite_listings.add(listing_2)

        self.assertIn(listing_1, user.favourite_listings.all())
        self.assertIn(listing_2, user.favourite_listings.all())
