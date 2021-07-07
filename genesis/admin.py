from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ("name","about","item_type_keywords","created_at","updated_at")

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name","item_type","about","image","item_keywords","created_at","updated_at")

@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display= ("name","value_in_kg","created_at","updated_at")

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("name","address_line_1","address_line_2","city","state","pincode","gst_number","delivery_instructions","created_by","created_at","updated_at")

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("name","address","contact_name","contact_number","max_quantity","weight_group","created_at","updated_at","created_by")

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display= ("name","item_type","inventory_name","quantity","weight_group","original_price_per_quantity","selling_price_per_quantity","minimum_order_quantity","status","keywords","created_at","updated_at","created_by")

@admin.register(OrderedItems)
class OrderedItemsAdmin(admin.ModelAdmin):
    list_display = ("number","invoice_id","order_status","inventory_name","quantity","weight_group","purchase_price_per_quantity","GST_applicable","rebate","cgst","sgst","igst","is_igst","total_price")
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("number","shipping_address","billing_address","payment_mode","payment_details","total_price","grand_total","created_by","created_at","updated_at")

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_filter = ("created_at","updated_at")
    list_display = ("item_name","quantity","billing_address","weight_group","seller_action_required","buyer_action_required","po_file","quote_file","status","created_by","created_at","updated_at")
    search_fields = ("id","created_by","created_at","updated_at")
    readonly_fields = ("id","created_at","updated_at")