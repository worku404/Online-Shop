from django import forms
from .models import Order
from .validators import validate_ethiopian_postal_code


class OrderCreateForm(forms.ModelForm):
    postal_code = forms.CharField(
        min_length=4,
        max_length=4,
        validators=[validate_ethiopian_postal_code],
    )

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]
