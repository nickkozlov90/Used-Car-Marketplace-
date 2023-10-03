from datetime import datetime

from django import forms

from marketplace.models import Brand, Model


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
