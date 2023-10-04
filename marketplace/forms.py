from datetime import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from marketplace.models import Brand, Model, Image, Listing

current_year = datetime.now().year
MIN_YEAR = 1970
YEARS = [('', '-----')] + [(str(year), str(year)) for year in range(MIN_YEAR, current_year + 1)]


class SearchForm(forms.Form):

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose a brand...'}),
        help_text="Select a brand"
    )

    model = forms.ModelChoiceField(
        queryset=Model.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': "Select a model"
        })
    )

    year_start = forms.ChoiceField(
        choices=YEARS,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose a brand...'})
    )

    year_end = forms.ChoiceField(
        choices=YEARS,
        required=False,
        widget=forms.Select(
            attrs={'class': 'form-control', 'placeholder': 'Choose a brand...'}
        )
    )

    price_start = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "min": "0",
            'class': 'form-control', 'placeholder': 'Set minimal price...'}
        )
    )

    price_end = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "min": "0",
            'class': 'form-control', 'placeholder': 'Set maximal price...'}
        )
    )

    mileage_start = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "min": "0",
            'class': 'form-control', 'placeholder': 'Set minimal mileage...'}
        )
    )

    mileage_end = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            "min": "0",
            'class': 'form-control', 'placeholder': 'Set maximal mileage...'}
        )
    )


class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = "__all__"

    car_model = forms.ModelChoiceField(
        queryset=Model.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    year = forms.IntegerField(
        validators=[
            MinValueValidator(MIN_YEAR),
            MaxValueValidator(current_year)
        ],
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter a year',
                "min": MIN_YEAR,
                "max": current_year
            }
        ),
    )
    price = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(
            attrs={"placeholder": "Enter a price in $", "min": 0}
        ),
    )
    mileage = forms.IntegerField(
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(
            attrs={"placeholder": "Enter a mileage in km", "min": 0}
        ),
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Describe your car"}
        )
    )

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields["seller"].required = False
        self.fields["seller"].widget = forms.HiddenInput()


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
