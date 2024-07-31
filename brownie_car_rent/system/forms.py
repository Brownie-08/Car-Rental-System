from django import forms
from .models import Car, Order, PrivateMsg

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = [
            "image",
            "car_name",
            "company_name",
            "num_of_seats",
            "cost_par_day",
            "content",
        ]
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "car_name",
            "dealer_name",
            "cell_no",
            "address",
            "date_from",
            "date_to",
        ]
        widgets = {
            'date_from': forms.DateInput(attrs={'type': 'date'}),
            'date_to': forms.DateInput(attrs={'type': 'date'}),
        }
class MessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMsg
        fields = [
            "name",
            "email",
            "message",
        ]
