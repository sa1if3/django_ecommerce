from django.urls import include, path
from shoppingcart import views
urlpatterns = [
    path('shopping_cart/',views.shopping_cart, name = "shopping_cart"),
    path('public_listing/',views.public_listing, name = "public_listing"),
    path('search_listing/',views.search_listing, name = "search_listing"),
    # path('public_add_to_cart/',views.public_add_to_cart, name = "public_add_to_cart"),
    path('public_form_add_to_cart/',views.public_form_add_to_cart, name = "public_form_add_to_cart"),
    path('public_destroy_from_cart/<int:id>',views.public_destroy_from_cart, name = "public_destroy_from_cart"),
    path('public_total_cart/',views.public_total_cart, name = "public_total_cart"),
    path('checkout/',views.checkout, name = "checkout"),
    path('place_order/',views.place_order, name = "place_order"),
    #path('checkout_confirmation/',views.checkout_confirmation, name = "checkout_confirmation"),
    
]