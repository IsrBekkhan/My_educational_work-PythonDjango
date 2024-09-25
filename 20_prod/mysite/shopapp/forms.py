from django import forms

from shopapp.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"

    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),
    )


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
