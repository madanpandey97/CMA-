from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':"Your Street Address",
        'class' : 'form-control'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder':"Your Apartment Address",
        'class': 'form-control'
    }))
    country = CountryField(blank_label='(select country)').formfield( widget=CountrySelectWidget(attrs={
        'class':"custom-select d-block w-100"
    }))
    pincode = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Pincode',
        'class': 'form-control'
    }))
    same_billing_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget=forms.RadioSelect,
                                       choices=PAYMENT_CHOICES)
