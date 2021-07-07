from typing import List
from django import forms
from shoppingcart.models import Cart
from genesis.models import Order, OrderedItems
from django.contrib.admin import widgets
from django.forms.widgets import CheckboxInput


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['listing', 'total_quantity', 'created_by']

    def __init__(self, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields['total_quantity'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-border'


class OrderForm(forms.ModelForm):
    number = forms.CharField(max_length=100, required=False)
    payment_details = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Order
        fields = ['number', 'shipping_address', 'billing_address', 'payment_status', 'payment_mode',
                  'payment_details', 'item_details', 'total_price', 'grand_total', 'created_by']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['shipping_address'].required = True
        self.fields['billing_address'].required = True
        self.fields['item_details'].required = False

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-border'
