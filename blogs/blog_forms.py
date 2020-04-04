from django import  forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES=(
	# ('s', 'Stripe'),
	('P', 'PayPal'),
	)


class CheckoutForm(forms.Form):
	street_address = forms.CharField(widget=forms.TextInput(attrs={
		"placeholder": "Main Posting Address",
		'class':'col-md-11 pt-3'
		}))
	apartment_address = forms.CharField(required= False, widget=forms.TextInput(attrs={
		"placeholder": "apartment or suite", 
		'class':'col-md-11 pt-3'
		}))
	country = CountryField(blank_label='(select country)').formfield(widget =CountrySelectWidget(attrs={
		'class': 'custom-select d-block w-100'
		}))
	zip =forms.CharField(widget=forms.TextInput(attrs={
		'class':'form-control'
		}))
	same_biling_address = forms.BooleanField(required=False)
	save_info = forms.BooleanField(required=False)
	payment_options=forms.ChoiceField(widget=forms.RadioSelect,
						choices=PAYMENT_CHOICES)

