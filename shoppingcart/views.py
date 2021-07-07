from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from shoppingcart.forms import *
from shoppingcart.models import *
from genesis.models import Listing, Address, Order, OrderedItems, Weight
# from django.contrib.admin import widgets
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.db import transaction
from django.conf import settings
from .tasks import send_notification_email_task, send_notification_single_sms_task
# Create your views here.


@login_required(login_url="user_login")
def shopping_cart(request):
    cart = Cart.objects.select_related("listing").filter(created_by=request.user.id)
    return render(request, 'shoppingcart/cart/show.html', {'cart': cart})

# Start Public Listing


# @login_required(login_url="user_login")
def search_listing(request):
    return render(request, 'shoppingcart/publiclisting/search.html')


# @login_required(login_url="user_login")
def public_listing(request):
    query = request.GET.get('search')
    items = ""
    address = ""
    weight = ""
    try:
        if request.user.is_authenticated:
            item = Listing.objects.select_related("item_type","inventory_name","weight_group").filter(Q(~Q(created_by=request.user.id),
                                                        status="PUBLIC", name__icontains=query) | Q(~Q(created_by=request.user.id),status="PUBLIC",item_type__name__icontains=query))
        else:
            item = Listing.objects.select_related("item_type","inventory_name","weight_group").filter(Q(status="PUBLIC", name__icontains=query) | Q(status="PUBLIC",item_type__name__icontains=query))
        address = Address.objects.filter(created_by = request.user.id)
        weight = Weight.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(item, 10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
    except Exception as e:
        messages.error(request, str(e))

    return render(request, 'shoppingcart/publiclisting/show.html', {'items': items, 'query': query, 'address':address, 'weight':weight})


# @login_required(login_url="user_login")
# def public_add_to_cart(request):
#     if request.method == "POST":
#         tq = request.POST.get("quantity")
#         li = request.POST.get("id")
#         msg = "ACCESSED"
#         qty = 0
#         try:
#             listing_instance = Listing.objects.filter(id=li).first()
#             cart_temp = Cart.objects.filter(
#                 listing=listing_instance.id, created_by=request.user.id).first()
#             if cart_temp:
#                 sum = int(tq)+int(cart_temp.total_quantity)
#                 if sum < listing_instance.quantity:
#                     if sum < listing_instance.minimum_order_quantity:
#                         sum = listing_instance.minimum_order_quantity
#                     msg = "updated"
#                     qty = sum
#                     cart = Cart.objects.update_or_create(
#                         listing=listing_instance, created_by=request.user, defaults={'total_quantity': qty},)

#                 else:
#                     msg = "MAX_UPDATED"
#                     qty = listing_instance.quantity
#                     cart = Cart.objects.update_or_create(
#                         listing=listing_instance, created_by=request.user, defaults={'total_quantity': qty},)
#             else:
#                 msg = "added"
#                 qty = tq
#                 if int(qty) <= int(listing_instance.quantity):
#                     pass
#                 else:
#                     msg = "MAX_UPDATED"
#                     qty = listing_instance.quantity
#                 cart = Cart.objects.update_or_create(
#                     listing=listing_instance, created_by=request.user, defaults={'total_quantity': qty},)
#         except Exception as e:
#             messages.error(request, str(e))
#     responseData = {
#         'message': msg,
#         'quantity': qty,
#     }

#     return JsonResponse(responseData)

@login_required(login_url="user_login")
def public_form_add_to_cart(request):
    if request.method == "POST":
        tq = request.POST.get("total_quantity")
        li = request.POST.get("listing")
        msg = "ACCESSED"
        qty = 0
        try:
            listing_instance = Listing.objects.filter(id=li).first()
            cart_temp = Cart.objects.filter(
                listing=listing_instance.id, created_by=request.user.id).first()
            if cart_temp:  # Item already exists in cart
                sum = int(tq)+int(cart_temp.total_quantity)
                if sum < listing_instance.quantity:
                    if sum < listing_instance.minimum_order_quantity:
                        sum = listing_instance.minimum_order_quantity
                    msg = "updated"
                    qty = sum
                    data = request.POST.copy()
                    data['created_by'] = request.user.id
                    data['listing'] = listing_instance
                    data['total_quantity'] = qty
                    cart_form = CartForm(data, instance=cart_temp)
                    if cart_form.is_valid():
                        try:
                            cart_form.save()
                        except Exception as e:
                            messages.error(request, str(e))
                   # cart = Cart.objects.update_or_create(
                    #    listing=listing_instance, created_by=request.user, defaults={'total_quantity': qty},)

                else:
                    msg = "MAX_UPDATED"
                    qty = listing_instance.quantity
                    data = request.POST.copy()
                    data['created_by'] = request.user.id
                    data['listing'] = listing_instance
                    data['total_quantity'] = qty
                    cart_form = CartForm(data, instance=cart_temp)
                    if cart_form.is_valid():
                        try:
                            cart_form.save()
                        except Exception as e:
                            messages.error(request, str(e))
                    # cart = Cart.objects.update_or_create(
                    #    listing=listing_instance, created_by=request.user, defaults={'total_quantity': qty},)
            else:
                """ Start First time add item to cart
                If the cart item is added for the first time this part is used. 
                """
                msg = "added"
                qty = tq
                if int(qty) <= int(listing_instance.minimum_order_quantity):
                    qty = listing_instance.minimum_order_quantity
                    data = request.POST.copy()
                    data['created_by'] = request.user.id
                    data['listing'] = listing_instance
                    data['total_quantity'] = qty
                    cart_form = CartForm(data)
                    if cart_form.is_valid():
                        try:
                            cart_form.save()
                            responseData = {
                                'message': msg,
                                'quantity': qty,
                            }
                        except Exception as e:
                            messages.error(request, str(e))
                else:
                    msg = "MAX_UPDATED"
                    qty = listing_instance.quantity
                    data = request.POST.copy()
                    data['created_by'] = request.user.id
                    data['listing'] = listing_instance
                    data['total_quantity'] = qty
                    cart_form = CartForm(data, instance=cart_temp)
                    if cart_form.is_valid():
                        try:
                            cart_form.save()
                        except Exception as e:
                            messages.error(request, str(e))
                    # cart = Cart.objects.update_or_create(listing=listing_instance, created_by=request.user, defaults={'total_quantity': qty},)
        except Exception as e:
            messages.error(request, str(e))
            responseData = {
                'message': str(e),
                'quantity': qty,
            }
    responseData = {
        'message': msg,
        'quantity': qty,
    }

    return JsonResponse(responseData)


@login_required(login_url="user_login")
def public_destroy_from_cart(request, id):
    if request.method == "POST":
        cart = Cart.objects.filter(id=id, created_by=request.user.id).first()
        try:
            cart.delete()
            messages.success(request, 'Item removed from cart!')
        except Exception as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "Unauthorized Request!")
    return redirect("shopping_cart") 
    
@login_required(login_url="user_login")
def public_total_cart(request):
    cart = Cart.objects.filter(created_by=request.user.id).count()
    responseData = {
        'item_count': cart,
    }

    return JsonResponse(responseData)
# Stop Public Listing

# Start Checkout/Order


@login_required(login_url="user_login")
def checkout(request):
    if request.method == "POST":
        item_id = request.POST.getlist("itemID[]")
        item_quantity = request.POST.getlist("itemQTY[]")
        value_pair = {item_id[i]: item_quantity[i]
                      for i in range(len(item_id))}
        
        context = {}
        try:
            address = Address.objects.filter(created_by=request.user.id)
            cart = Cart.objects.select_related("listing","listing__weight_group").filter(
                created_by=request.user.id, pk__in=item_id)
            
            total = 0
            for obj in cart:
                total = int(
                    total) + int(obj.listing.selling_price_per_quantity) * int(obj.total_quantity)
            tax = 0.18  # 18% default
            gst = tax * total
            grand_total = total + gst
            context = {'value_pair': value_pair, 'address': address,
                       'cart': cart, 'total': total, 'tax': tax*100, 'grand_total': grand_total, 'gst': gst}
            return render(request, 'shoppingcart/checkout/show.html', context)
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'shoppingcart/checkout/show.html', context)


@login_required(login_url="user_login")
def place_order(request):
    if request.method == "POST":
        try:
            billing_address = Address.objects.get(id=request.POST.get("billing_address"))
            shipping_address = Address.objects.get(id=request.POST.get("shipping_address"))
            number = get_random_string(length=10, allowed_chars='ABC1234567890')
            payment_status = 'To Pay'
            payment_mode = 'Cash'
            # payment_details
            # Start Default
            total_price = 0
            rebate = 0
            cgst = 0
            sgst = 0
            igst = 0
            grand_total = 0
            invoice_id = 1
            # End Default
            created_by = request.user
            with transaction.atomic():
                data = request.POST.copy()
                data['billing_address'] = billing_address
                data['shipping_address'] = shipping_address
                data['number'] = number
                data['payment_status'] = payment_status
                data['payment_mode'] = payment_mode
                data['total_price'] = total_price
                data['grand_total'] = grand_total
                data['created_by'] = created_by
                order = OrderForm(data)
                if order.is_valid():
                    try:
                        order_saved = order.save()
                    except Exception as e:
                        messages.error(request, str(e))
                        return redirect('show_all_order')
                else:
                    messages.error(request,str(order.errors))
                # order = Order(billing_address=billing_address, shipping_address=shipping_address, number=number, payment_status=payment_status,
                #               payment_mode=payment_mode, total_price=total_price, grand_total=grand_total, created_by=created_by)
                # order.save()
                if order_saved:
                    item_id = request.POST.getlist("itemID[]")
                    total_price = 0
                    order_status = 'PLACED'
                    inv_id = 1
                    app_name = settings.APP_NAME
                    app_about = settings.APP_ABOUT
                    for temp in range(len(item_id)):
                        cart_name = Cart.objects.get(
                            id=item_id[temp], created_by=request.user.id)
                        listing_update = Listing.objects.get(
                            id=cart_name.listing.id)
                        item_name = cart_name.listing
                        weight_group = cart_name.listing.weight_group
                        inventory_name = cart_name.listing.inventory_name
                        purchase_price_per_quantity = cart_name.listing.selling_price_per_quantity
                        quantity = cart_name.total_quantity
                        # check if quantity still exists in stock or delete item from cart
                        temp_quantity = listing_update.quantity - quantity
                        individual_total_price = purchase_price_per_quantity * \
                            quantity  # OrderedItems table
                        order_update_status = False
                        GST_applicable = True
                        is_igst = False
                        # start price update
                        tax = 0.18  # 18% default
                        tax = tax/2  # 9% each
                        temp = tax * individual_total_price
                        cgst = temp
                        sgst = temp
                        igst = temp
                        rebate = 0
                        total_price += purchase_price_per_quantity * quantity  # order table
                        grand_total += individual_total_price + \
                            (2*temp)  # order table
                        invoice_id = str(number)+"-"+str(inv_id)
                        inv_id += 1
                        # end price update
                        if temp_quantity >= 0:
                            # Add form here 2
                            ordered_items = OrderedItems(number=number, item_name=item_name, quantity=quantity, weight_group=weight_group,
                                                        inventory_name=inventory_name, purchase_price_per_quantity=purchase_price_per_quantity, order_status=order_status, GST_applicable=GST_applicable, rebate=rebate, cgst=cgst, sgst=sgst, igst=igst, is_igst=is_igst, invoice_id=invoice_id, total_price=individual_total_price)
                            ordered_items.save()
                            order_saved.item_details.add(ordered_items)
                            order_update_status = True
                            # Seller Email Start
                            temp_grand_total = ordered_items.total_price + \
                                (ordered_items.cgst*2)
                            subject = "New Order #" + \
                                str(ordered_items.invoice_id)+" Placed!"
                            message = f'Congratulations on receiving a new order of [{ordered_items.item_name.name}] for [{ordered_items.quantity} {ordered_items.weight_group.name}]. Total of the order is amount is '+str(
                                temp_grand_total)+"/-"
                            context = {'app_about': app_about, 'message': message,
                                    'subject': subject, 'app_name': app_name, 'user': request.user.username}
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [
                                ordered_items.inventory_name.created_by.email, ]
                            send_notification_email_task.delay(
                                context, email_from, recipient_list, subject)
                            # Seller Email Stop
                            # Seller SMS Start
                            sms_message = f'Dear Customer, Thank you for using {app_name}. A booking with CN. No.: {ordered_items.invoice_id} having your INV. No. {temp_grand_total} is confirmed. Track your CN here: tracking.techmion.com - {app_name}'
                            inventory_mobile_number = ordered_items.inventory_name.contact_number
                            send_notification_single_sms_task.delay(
                                inventory_mobile_number, sms_message)
                            # Seller SMS Stop
                        cart_name.delete()  # clearing the cart
                        listing_update.quantity = listing_update.quantity - quantity
                        if listing_update.quantity < 0 and order_update_status:
                            listing_update.status = 'PRIVATE'  # notify admin critical attack also
                        elif listing_update.quantity == 0 and order_update_status:
                            listing_update.status = 'PRIVATE'
                            temp_grand_total = ordered_items.total_price + \
                                (ordered_items.cgst*2)
                            subject = "Listing has been marked private"
                            message = f"Your listing item {ordered_items.item_name.name} has been marked private! This was done because your available quantity is Zero. Please change the status manually."
                            context = {'app_about': app_about, 'message': message,
                                    'subject': subject, 'app_name': app_name, 'user': request.user.username}
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [
                                ordered_items.inventory_name.created_by.email, ]
                            send_notification_email_task.delay(
                                context, email_from, recipient_list, subject)
                        elif listing_update.quantity < listing_update.minimum_order_quantity and order_update_status:
                            listing_update.status = 'PRIVATE'
                            temp_grand_total = ordered_items.total_price + \
                                (ordered_items.cgst*2)
                            subject = "Listing has been marked private"
                            message = f"Your listing item {ordered_items.item_name.name} has been marked private! This was done because your available quantity is below minimum order quantity. Please change the status manually."
                            context = {'app_about': app_about, 'message': message,
                                    'subject': subject, 'app_name': app_name, 'user': request.user.username}
                            email_from = settings.EMAIL_HOST_USER
                            recipient_list = [
                                ordered_items.inventory_name.created_by.email, ]
                            send_notification_email_task.delay(
                                context, email_from, recipient_list, subject)
                        else:
                            pass
                        listing_update.save()

                    # start order update
                    order_saved.total_price = total_price
                    order_saved.grand_total = grand_total
                    order_saved.save()
                    # end order update
                    # Customer Email Start
                    subject = "New Order #"+str(order_saved.number)+" Placed!"
                    message = f'Thank you for you order. Your total is amount is '+str(
                        order_saved.grand_total)+"/-"
                    context = {'app_about': app_about, 'message': message,
                            'subject': subject, 'app_name': app_name, 'user': request.user.username}
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.user.email, ]
                    send_notification_email_task.delay(
                        context, email_from, recipient_list, subject)
                    # Customer Email Stop

                    str1 = 'Order with #'+str(order_saved.number)+" of amount "+str(
                        order_saved.grand_total)+"/- is successfully placed. Download invoice from My Orders!!"
                    messages.success(request, str1)
        except Exception as e:
            messages.error(request, str(e))
    return redirect('show_all_order')
# Stop Checkout
