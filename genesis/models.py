from django.db import models
from crum import get_current_user
from django.core.validators import MaxValueValidator, MinValueValidator,RegexValidator
from decimal import *

# Create your models here.


class ItemType(models.Model):
    name = models.CharField(max_length=200, null=True)
    about = models.CharField(max_length=500, blank=True, null=True)
    item_type_keywords = models.CharField(
        max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "1. Item Types"

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200, null=True)
    item_type = models.ForeignKey(
        ItemType, blank=True, null=True, default=None, on_delete=models.RESTRICT)
    about = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    item_keywords = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "2. Items"

    def __str__(self):
        return self.name


class Weight(models.Model):
    name = models.CharField(max_length=200, null=True)
    value_in_kg = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "3. Weight Groups"

    def __str__(self):
        return self.name

class Address(models.Model):
    name = models.CharField(max_length=200, null=True)
    address_line_1 = models.CharField(max_length=200, null=True, blank=True)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=100, null=True, blank=True)
    contact_name = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=10)
    delivery_instructions = models.CharField(
        max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "4. Address/Billing Informations"

    def __str__(self):
        return self.name

class Inventory(models.Model):
    name = models.CharField(max_length=200, null=True)
    address = models.ForeignKey(
        Address, null=True, default=None, on_delete=models.RESTRICT)
    contact_name = models.CharField(max_length=100, null=True)
    contact_number = models.CharField(max_length=10, null=True)
    max_quantity = models.PositiveIntegerField(
        default=1, null=True, blank=True)
    weight_group = models.ForeignKey(
        Weight, null=True, default=None, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "5. Inventories"

    def __str__(self):
        return self.name


class Listing(models.Model):
    STATUS = (
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    )
    name = models.CharField(max_length=200, null=True)
    item_type = models.ForeignKey(
        Item, null=True, default=None, on_delete=models.RESTRICT)
    inventory_name = models.ForeignKey(
        Inventory, default=None, on_delete=models.RESTRICT, null=True)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    weight_group = models.ForeignKey(
        Weight, blank=True, null=True, default=None, on_delete=models.RESTRICT)
    original_price_per_quantity = models.PositiveIntegerField(default=1)
    selling_price_per_quantity = models.PositiveIntegerField(default=1)
    minimum_order_quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    about = models.CharField(max_length=500, blank=True, null=True)
    keywords = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "6. Listings"

    def __str__(self):
        return self.name

class OrderedItems(models.Model):
    ORDER_STATUS = (
        ('PLACED', 'Placed'),
        ('ACCEPTED', 'Accepted'),
        ('PACKED', 'Packed'),
        ('SHIPPED', 'Shipped'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    )
    number = models.CharField(max_length=100, null=True)
    invoice_id = models.CharField(max_length=100, null=True)
    item_name = models.ForeignKey(
        Listing, blank=True, null=True, default=None, on_delete=models.RESTRICT)
    inventory_name = models.ForeignKey(
        Inventory, default=None, on_delete=models.RESTRICT, null=True)
    GST_applicable = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1)
    is_igst = models.BooleanField(default=False)
    rebate = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, validators=[
                                 MinValueValidator(Decimal('0.00'))])
    cgst = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, validators=[
                               MinValueValidator(Decimal('0.01'))])
    sgst = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, validators=[
                               MinValueValidator(Decimal('0.01'))])
    igst = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=12, validators=[
                               MinValueValidator(Decimal('0.01'))])
    weight_group = models.ForeignKey(
        Weight, blank=True, null=True, default=None, on_delete=models.RESTRICT)
    purchase_price_per_quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField(default=1)
    order_status = models.CharField(
        max_length=200, null=True, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = "7. Ordered Items"

    def __str__(self):
        return self.item_name.name

class Order(models.Model):
    PAYMENT_STATUS = (
        ('Paid', 'Paid'),
        ('To Pay', 'To Pay'),
        ('Failed', 'Failed'),
    )
    PAYMENT_MODE = (
        ('Cash', 'Cash'),
        ('NEFT', 'NEFT'),
        ('RTGS', 'RTGS'),
        ('Cheque', 'Cheque'),
        ('Payment Gateway', 'Payment Gateway'),
    )
    number = models.CharField(max_length=100, null=True, unique=True)
    shipping_address = models.ForeignKey(
        Address, blank=True, null=True, default=None, on_delete=models.RESTRICT, related_name='shipping')
    billing_address = models.ForeignKey(
        Address, blank=True, null=True, default=None, on_delete=models.RESTRICT, related_name='billing')
    payment_status = models.CharField(
        max_length=200, null=True, choices=PAYMENT_STATUS)
    payment_mode = models.CharField(
        max_length=200, null=True, choices=PAYMENT_MODE)
    payment_details = models.CharField(max_length=200, blank=True, null=True)
    item_details = models.ManyToManyField(OrderedItems)
    total_price = models.PositiveIntegerField(default=1)
    grand_total = models.DecimalField(decimal_places=2, max_digits=12, validators=[
                                      MinValueValidator(Decimal('0.00'))])
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "8. Order/Transactions"
    def __str__(self):
        return self.number

class Quote(models.Model):
    STATUS = (
        ('QUOTE_SENT', 'Quote Sent'),
        ('PURCHASE_ORDER_SENT', 'Purchase Order Sent'),
        ('RECEIVED', 'Quote Request Received'),
        ('CANCELLED','Cancelled'),
        ('COMPLETED','Completed'),
    )
    item_name = models.ForeignKey(
        Listing, blank=True, null=True, default=None, on_delete=models.RESTRICT)
    weight_group = models.ForeignKey(
        Weight, null=True, default=None, on_delete=models.RESTRICT)
    billing_address = models.ForeignKey(
        Address, blank=True, null=True, default=None, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=1)
    seller_action_required = models.BooleanField(default=True)
    buyer_action_required = models.BooleanField(default=False)
    po_file = models.FileField(upload_to='documents/po/',blank=True)
    quote_file = models.FileField(upload_to='documents/qo/',blank=True)
    invoice_file = models.FileField(upload_to='documents/in/',blank=True)
    delivery_receipt_file = models.FileField(upload_to='documents/dr/',blank=True)
    status = models.CharField(
        max_length=50, null=True, blank=True, choices=STATUS)
    created_by = models.ForeignKey(
        'auth.User', blank=True, null=True, default=None, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "9. Request Quotes"

    def __str__(self):
        return str(self.id)