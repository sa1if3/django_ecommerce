from django.urls import path
from genesis import views
from django.views.generic import RedirectView
urlpatterns = [
    path('', RedirectView.as_view(url='search_listing')),
    path('',views.dashboard, name = "home"),
    path('dashboard/',views.dashboard, name = "dashboard"),
    # Start Address URL
    path('add_new_address/',views.add_new_address, name = "add_new_address"),
    path('show_all_address/',views.show_all_address, name = "show_all_address"),
    path('delete_address/<int:id>', views.destroy_address,name="delete_address"),
    path('edit_address/<int:id>', views.edit_address, name = "edit_address"),  
    path('update_address/<int:id>', views.update_address, name = "update_address"),
    # End Address URL
    # Start Inventory URL
    path('add_new_inventory/',views.add_new_inventory, name = "add_new_inventory"),
    path('show_all_inventory/',views.show_all_inventory, name = "show_all_inventory"),
    path('delete_inventory/<int:id>', views.destroy_inventory,name="delete_inventory"),
    path('edit_inventory/<int:id>', views.edit_inventory, name = "edit_inventory"),  
    path('update_inventory/<int:id>', views.update_inventory, name = "update_inventory"),
    # End Inventory URL
    # Start Listing URL
    path('add_new_listing/',views.add_new_listing, name = "add_new_listing"),
    path('show_all_listing/',views.show_all_listing, name = "show_all_listing"),
    path('delete_listing/<int:id>', views.destroy_listing,name="delete_listing"),
    path('edit_listing/<int:id>', views.edit_listing, name = "edit_listing"),  
    path('update_listing/<int:id>', views.update_listing, name = "update_listing"),
    # End Listing URL
    # Start Order URL
    path('show_all_order/',views.show_all_order, name = "show_all_order"),
    path('show_my_customer_orders/',views.show_my_customer_orders, name = "show_my_customer_orders"),
    path('change_order_status/<int:id>', views.change_order_status, name = "change_order_status"),
    # End Order URL
    path('generate_invoice/<int:id>',views.generate_invoice, name = "generate_invoice"),
    path('generate_invoice_ordered/<int:id>',views.generate_invoice_ordered, name = "generate_invoice_ordered"),
    path('generate_seller_invoice_ordered/<int:id>',views.generate_seller_invoice_ordered, name = "generate_seller_invoice_ordered"),
    # Start Quote URL
    path('add_new_quote/',views.add_new_quote, name = "add_new_quote"),
    path('show_all_sent_quote/',views.show_all_sent_quote, name = "show_all_sent_quote"),
    path('show_all_received_quote/',views.show_all_received_quote, name = "show_all_received_quote"),
    path('edit_purchase_order/<int:id>', views.edit_purchase_order, name = "edit_purchase_order"),
    path('update_purchase_order/<int:id>', views.update_purchase_order, name = "update_purchase_order"),
    path('edit_quote_order/<int:id>', views.edit_quote_order, name = "edit_quote_order"),
    path('update_quote_order/<int:id>', views.update_quote_order, name = "update_quote_order"),
    path('edit_dr_invoice/<int:id>', views.edit_dr_invoice, name = "edit_dr_invoice"),
    path('update_dr_invoice/<int:id>', views.update_dr_invoice, name = "update_dr_invoice"),
    # path('delete_quote/<int:id>', views.destroy_quote,name="delete_quote"),
    # path('edit_quote/<int:id>', views.edit_quote, name = "edit_quote"),  
    # End Quote URL
]