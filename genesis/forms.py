from django import forms
from genesis.models import *
from django.contrib.admin import widgets
from django.forms.widgets import CheckboxInput
from django.core.validators import RegexValidator, ValidationError


class AddressForm(forms.ModelForm):
    name = forms.CharField(min_length=5, max_length=200)
    address_line_1 = forms.CharField(min_length=20, max_length=200)
    address_line_2 = forms.CharField(
        min_length=10, max_length=200, required=False)
    city = forms.CharField(min_length=5, max_length=100)
    state = forms.CharField(min_length=5, max_length=100)
    pincode = forms.CharField(min_length=6, validators=[RegexValidator(
        '^[1-9][0-9]{5}$', message="Enter a Valid Indian Pincode")])
    gst_number = forms.CharField(max_length=100, required=False, validators=[RegexValidator(
        '\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}', message="Enter a Valid Indian GST Number")])
    contact_name = forms.CharField(min_length=5, max_length=100)
    contact_number = forms.CharField(min_length=10, max_length=10, validators=[RegexValidator(
        '^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$', message="Enter a Valid Indian Phone Number")])
    delivery_instructions = forms.CharField(
        min_length=10, max_length=100, required=False)

    class Meta:
        model = Address
        fields = ['name', 'address_line_1', 'address_line_2', 'city', 'state', 'pincode', 'gst_number', 'contact_name',
                  'contact_number', 'delivery_instructions', 'created_by', 'is_default']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-border'


class InventoryForm(forms.ModelForm):
    name = forms.CharField(min_length=5, max_length=200)
    contact_name = forms.CharField(min_length=5, max_length=100)
    contact_number = forms.CharField(min_length=10, max_length=10, validators=[RegexValidator(
        '^(?:(?:\+|0{0,2})91(\s*[\ -]\s*)?|[0]?)?[789]\d{9}|(\d[ -]?){10}\d$', message="Enter a Valid Indian Phone Number")])

    class Meta:
        model = Inventory
        fields = ['name', 'address', 'contact_name', 'contact_number',
                  'max_quantity', 'weight_group', 'created_by']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(InventoryForm, self).__init__(*args, **kwargs)
        self.fields['weight_group'].required = True
        self.fields['address'].required = True
        self.fields["address"].queryset = Address.objects.filter(
            created_by=self.user.id)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-border'


class ListingForm(forms.ModelForm):
    name = forms.CharField(min_length=5, max_length=200)
    about = forms.CharField(min_length=50, max_length=500, required=True)
    keywords = forms.CharField(min_length=10, max_length=200, required=False)

    class Meta:
        model = Listing
        fields = ['name', 'item_type', 'inventory_name', 'quantity', 'image', 'weight_group', 'selling_price_per_quantity',
                  'minimum_order_quantity', 'status', 'about', 'keywords', 'created_by']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['weight_group'].required = True
        self.fields['item_type'].required = True
        self.fields['inventory_name'].required = True
        self.fields["inventory_name"].queryset = Inventory.objects.filter(
            created_by=self.user.id)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-border'


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ["item_name", "quantity", "seller_action_required", "buyer_action_required",
                  "po_file", "quote_file", "status", "created_by", "delivery_receipt_file", "invoice_file","billing_address","weight_group"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(QuoteForm, self).__init__(*args, **kwargs)
        self.fields['item_name'].required = True
        self.fields['quantity'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-border'
