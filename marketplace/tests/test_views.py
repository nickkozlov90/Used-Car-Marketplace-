from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from marketplace.models import MarketUser, Listing, Model, Brand

LISTINGS_URL = reverse("marketplace:listings-list")


class PublicMarketUserTests(TestCase):
    def test_login_required(self):
        response = self.client.get(
            reverse("marketplace:market-user-detail", args=[1])
        )

        self.assertNotEqual(response.status_code, 200)

    def test_create_market_user(self):
        form_data = {
            "first_name": "test First",
            "last_name": "test_last",
            "username": "test_username_1",
            "password1": "test$23456789",
            "password2": "test$23456789",
            "phone_number": "+380963334576",
            "profile_picture": "",
        }

        self.client.post(
            reverse("marketplace:market-user-create"),
            data=form_data
        )
        new_market_user = MarketUser.objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_market_user.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_market_user.phone_number,
            form_data["phone_number"]
        )


class PrivateMarketUserTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test$23456789",
            phone_number="+380961234576",
            profile_picture=None,
        )

        self.client.force_login(self.user)

    def test_update_market_user(self):
        market_user = MarketUser.objects.create_user(
            first_name="test First",
            last_name="test Last",
            username="test_username_1",
            password="test$23456789",
            phone_number="+380963334576",
            profile_picture=None,
        )
        new_last_name = "new_last_name"
        response = self.client.post(
            reverse(
                "marketplace:market-user-update",
                kwargs={"pk": market_user.id}
            ),
            data={
                "last_name": new_last_name,
                "username": "test_username_1",
                "phone_number": "+380963334576",
            },
        )
        self.assertEqual(response.status_code, 302)
        market_user.refresh_from_db()
        updated_market_user = MarketUser.objects.get(id=market_user.id)
        self.assertEqual(updated_market_user.last_name, new_last_name)

    def test_assign_listing_to_favourite_if_not_assigned(self):
        market_user = get_user_model().objects.get(id=self.user.id)

        brand = Brand.objects.create(name="test_brand")
        model = Model.objects.create(brand=brand, name="test_model")

        listing = Listing.objects.create(
            seller=self.user,
            car_model=model,
            year=2020,
            price=15000,
            mileage=50000,
            description="test_description_1",
        )

        self.assertFalse(
            get_user_model().objects.filter(id=market_user.id).get()
            in listing.users.all()
        )

        response = self.client.get(
            reverse(
                "marketplace:toggle-assign-to-listing",
                kwargs={"pk": market_user.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(
            get_user_model().objects.filter(id=market_user.id).get(),
            listing.users.all()
        )

    def test_remove_listing_if_assigned_to_driver_favourites(self):
        market_user = get_user_model().objects.get(id=self.user.id)

        brand = Brand.objects.create(name="test_brand")
        model = Model.objects.create(brand=brand, name="test_model")

        listing = Listing.objects.create(
            seller=self.user,
            car_model=model,
            year=2020,
            price=15000,
            mileage=50000,
            description="test_description_1",
        )
        market_user.favourite_listings.add(listing)
        market_user.save()

        self.assertIn(
            get_user_model().objects.get(id=market_user.id),
            listing.users.all()
        )

        response = self.client.get(
            reverse(
                "marketplace:toggle-assign-to-listing",
                kwargs={"pk": market_user.id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(
            get_user_model().objects.get(id=market_user.id),
            listing.users.all()
        )


class PublicListingTests(TestCase):
    def test_login_required(self):
        response = self.client.get(LISTINGS_URL)

        self.assertEqual(response.status_code, 200)

    def test_retrieve_listings(self):
        response = self.client.get(LISTINGS_URL)
        listings = Listing.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["listings"]), list(listings))
        self.assertTemplateUsed(response, "marketplace/listing_list.html")


class PrivateListingCase(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test$23456789",
            phone_number="+380961234576",
            profile_picture=None,
        )

        self.client.force_login(self.user)

    def test_create_listing(self):
        brand = Brand.objects.create(name="test_brand")
        model = Model.objects.create(brand=brand, name="test_model")

        form_data = {
            "car_model": model.id,
            "seller": self.user.id,
            "year": 2020,
            "price": 15000,
            "mileage": 50000,
            "description": "test_description",
            "images-TOTAL_FORMS": 0,
            "images-INITIAL_FORMS": 0,
        }

        response = self.client.post(
            reverse("marketplace:listing-create"), data=form_data
        )
        new_listing = Listing.objects.get(car_model=form_data["car_model"])

        self.assertEqual(response.status_code, 302)
        self.assertEqual(new_listing.car_model.id, form_data["car_model"])
        self.assertEqual(new_listing.seller.id, self.user.id)

    def test_update_listing(self):
        brand = Brand.objects.create(name="test_brand")
        model = Model.objects.create(brand=brand, name="test_model")

        listing = Listing.objects.create(
            seller=self.user,
            car_model=model,
            year=2020,
            price=15000,
            mileage=50000,
            description="test_description_1",
        )
        new_price = 20000
        response = self.client.post(
            reverse("marketplace:listing-update", kwargs={"pk": listing.id}),
            data={
                "seller": self.user.id,
                "car_model": model.id,
                "year": 2021,
                "price": new_price,
                "mileage": 50000,
                "description": "test_description_1",
                "images-TOTAL_FORMS": 0,
                "images-INITIAL_FORMS": 0,
            },
        )

        listing.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(listing.price, new_price)

    def test_delete_listing(self):
        brand = Brand.objects.create(name="test_brand")
        model = Model.objects.create(brand=brand, name="test_model")
        listing = Listing.objects.create(
            seller=self.user,
            car_model=model,
            year=2020,
            price=15000,
            mileage=50000,
            description="test_description_1",
        )

        response = self.client.post(
            reverse("marketplace:listing-delete", kwargs={"pk": listing.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Listing.objects.filter(id=listing.id).exists())

    def test_listing_pagination_is_five(self):
        number_of_listing = 7

        for listing_id in range(number_of_listing):
            brand = Brand.objects.create(name=f"test_brand_{listing_id}")
            model = Model.objects.create(
                brand=brand,
                name=f"test_model_{listing_id}"
            )
            Listing.objects.create(
                seller=self.user,
                car_model=model,
                price=f"{listing_id}0000",
                year=f"200{listing_id}",
                mileage=f"{listing_id}00000",
                description=f"test_description_{listing_id}",
            )

        response = self.client.get(
            reverse("marketplace:listings-list") + "?page=2"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["listings"]), 2)

    def test_retrieve_sale_listings(self):
        number_of_listing = 3

        for listing_id in range(number_of_listing):
            brand = Brand.objects.create(name=f"test_brand_{listing_id}")
            model = Model.objects.create(
                brand=brand,
                name=f"test_model_{listing_id}"
            )
            Listing.objects.create(
                seller=self.user,
                car_model=model,
                price=f"{listing_id}0000",
                year=f"200{listing_id}",
                mileage=f"{listing_id}00000",
                description=f"test_description_{listing_id}",
            )

        response = self.client.get(
            reverse("marketplace:sale-listings",
                    kwargs={"pk": self.user.id}
                    )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(list(response.context["listings"])),
            number_of_listing
        )
        self.assertTemplateUsed(response, "marketplace/listing_list.html")


class PasswordChangeTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            first_name="test First",
            last_name="test Last",
            username="test_username",
            password="test$23456789",
            phone_number="+380961234576",
            profile_picture=None,
        )

        self.client.force_login(self.user)

    def test_with_valid_data(self):
        new_password = "test$23456790"
        form_data = {
            "old_password": "test$23456789",
            "new_password1": new_password,
            "new_password2": new_password,
        }

        response = self.client.post(
            reverse("marketplace:password_change"), data=form_data
        )
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.check_password(new_password))

    def test_with_invalid_old_password(self):
        new_password = "test$23456790"
        form_data = {
            "old_password": "test$23456790",
            "new_password1": new_password,
            "new_password2": new_password,
        }

        response = self.client.post(
            reverse("marketplace:password_change"), data=form_data
        )
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Your old password was entered incorrectly.",
            str(response.content)
        )
        self.assertTrue(self.user.check_password("test$23456789"))

    def test_with_invalid_second_new_password(self):
        new_password = "test$23456790"
        form_data = {
            "old_password": "test$23456789",
            "new_password1": new_password,
            "new_password2": "test$23456791",
        }

        response = self.client.post(
            reverse("marketplace:password_change"), data=form_data
        )
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "The two password fields didn\\xe2\\x80\\x99t match.",
            str(response.content)
        )
