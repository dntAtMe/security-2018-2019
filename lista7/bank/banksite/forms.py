from django import forms
from .models import Payment


class PaymentValidationForm(forms.ModelForm):
	class Meta:
		model = Payment
		fields = ['title', 'content','value','account']
