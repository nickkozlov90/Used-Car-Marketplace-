from django.core.exceptions import ValidationError
from django.test import TestCase
from marketplace.forms import MarketUserCreationForm, validate_phone_number, ListingForm, SearchForm, current_year
from marketplace.models import MarketUser, Brand, Model


class SearchFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        brand = Brand.objects.create(name="test_brand")
        model = Model.objects.create(brand=brand, name="test_model")
        cls.form_data = {
            'brand': brand,
            'model': model,
            'year_start': '2020',
            'year_end': '2022',
            'price_start': '10000',
            'price_end': '20000',
            'mileage_start': '0',
            'mileage_end': '50000',
        }

    def test_valid_form(self):
        form = SearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_model_choice_field_queryset(self):
        form = SearchForm()
        self.assertEqual(len(form.fields['brand'].queryset), 1)
        self.assertEqual(len(form.fields['model'].queryset), 1)

    def test_empty_model_field(self):
        self.form_data['model']: ''
        form = SearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_empty_year_start_field(self):
        self.form_data['year_start']: ''
        form = SearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_empty_price_end_field(self):
        self.form_data['price_end']: ''
        form = SearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_edge_min_year_invalid(self):
        self.form_data['year_start'] = 1969
        form = SearchForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_edge_min_year_valid(self):
        self.form_data['year_start'] = 1970
        form = SearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_edge_min_price_valid(self):
        self.form_data['price_start'] = 0
        form = SearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_edge_min_mileage_valid(self):
        self.form_data['mileage_start'] = 0
        form = SearchForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_year_choices(self):
        form = SearchForm()

        year_start_choices = form.fields['year_start'].choices
        year_end_choices = form.fields['year_end'].choices

        year_start_values = [choice[0] for choice in year_start_choices]
        year_end_values = [choice[0] for choice in year_end_choices]

        expected_years = [""] + [str(year) for year in range(1970, current_year + 1)]
        self.assertEqual(year_start_values, expected_years)
        self.assertEqual(year_end_values, expected_years)


class ListingFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        cls.form_data = {
            "seller": seller,
            "car_model": model,
            'year': 2020,
            'price': 15000,
            'mileage': 50000,
            "description": "test_description",
        }

    def test_valid_data(self):
        form = ListingForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_year_low(self):
        self.form_data["year"] = 1960
        form = ListingForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('year', form.errors)

    def test_invalid_year_high(self):
        self.form_data["year"] = 2025
        form = ListingForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('year', form.errors)

    def test_invalid_price_negative(self):
        self.form_data["price"] = -1000
        form = ListingForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_invalid_mileage_negative(self):
        self.form_data["mileage"] = -1000
        form = ListingForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('mileage', form.errors)

    def test_invalid_car_model(self):
        self.form_data["car_model"] = 999
        form = ListingForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('car_model', form.errors)

    def test_empty_car_model(self):
        self.form_data["car_model"] = None
        form = ListingForm(data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('car_model', form.errors)

    def setUp(self):
        # Create some Model instances that will be used as choices in the form
        brand = Brand.objects.create(name="TestBrand")
        self.model1 = Model.objects.create(name='Model A', brand=brand)
        self.model2 = Model.objects.create(name='Model B', brand=brand)
        self.model3 = Model.objects.create(name='Model C', brand=brand)

    def test_display_available_options(self):
        form = ListingForm()
        car_model_choices = form.fields['car_model'].widget.choices

        available_choices = [choice[1] for choice in car_model_choices]

        self.assertIn('TestBrand Model A', available_choices)
        self.assertIn('TestBrand Model B', available_choices)
        self.assertIn('TestBrand Model C', available_choices)

    def test_seller_field_hidden_and_not_required(self):
        form = ListingForm()
        self.assertTrue(form.fields['seller'].widget.is_hidden)
        self.assertFalse(form.fields['seller'].required)


class MarketUserCreationFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            "first_name": "test First",
            "last_name": "test Last",
            "username": "test_username",
            "password1": "test$23456789",
            "password2": "test$23456789",
            "phone_number": "+380961234576",
            "profile_picture": None
        }

    def test_driver_creation_form_with_valid_data(self):
        form = MarketUserCreationForm(data=self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_driver_creation_form_with_invalid_data(self):
        modified_form_data = self.form_data.copy()
        modified_form_data["phone_number"] = "+380961234576XY"
        form = MarketUserCreationForm(data=modified_form_data)
        self.assertFalse(form.is_valid())


class ValidatePhoneNumberTest(TestCase):
    def test_length_more_than_13_characters(self):
        with self.assertRaisesMessage(
                ValidationError,
                "Ensure the phone number consist of 13 characters"
        ):
            phone_number = "+38096125987654"
            validate_phone_number(phone_number)

    def test_length_less_than_8_characters(self):
        with self.assertRaisesMessage(
                ValidationError,
                "Ensure the phone number consist of 13 characters"
        ):
            phone_number = "+380961259"
            validate_phone_number(phone_number)

    def test_starts_with_country_code(self):
        with self.assertRaisesMessage(
                ValidationError,
                "Ensure the phone number starts with '+380'"
        ):
            phone_number = "+340961259956"
            validate_phone_number(phone_number)

    def test_contains_only_digits_and_plus_sign(self):
        with self.assertRaisesMessage(
                ValidationError,
                "Ensure the phone number contains only '+' and digits"
        ):
            phone_number = "+3809612599ab"
            validate_phone_number(phone_number)
