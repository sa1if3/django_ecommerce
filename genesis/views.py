from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from genesis.forms import *
from genesis.models import *
from django.contrib.admin import widgets
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, request
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.conf import settings
from shoppingcart.tasks import send_notification_email_task, send_notification_single_sms_task
# Create your views here.

@login_required(login_url="user_login")
def generate_seller_invoice_ordered(request, id):
    # copy of generate_invoice_ordered
    # Generate PDF
    # Model data
    order = OrderedItems.objects.get(id=id)
    main_order = Order.objects.get(number=order.number)
    if main_order:
        tax = 0.9  # CGST + SGST = 18% default
        grand_total = (order.cgst * 2) + order.total_price
        context = {'order': order, 'tax': tax * 100,'main_order':main_order,'grand_total':grand_total}
    else:
        context ={}
    # Rendered
    html_string = render_to_string('genesis/order/pdf_ordered_items.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf(
        stylesheets=[
            # Change this to suit your css path
            str(settings.BASE_DIR) + '/static/order/css/main.css',
        ],)

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=' + \
        str(order.invoice_id)+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    # return render(request,'genesis/order/pdf.html')
    return response

@login_required(login_url="user_login")
def generate_invoice_ordered(request, id):
    # Generate PDF
    # Model data
    order = OrderedItems.objects.get(id=id)
    main_order = Order.objects.get(number=order.number,created_by=request.user.id)
    if main_order:
        tax = 0.9  # CGST + SGST = 18% default
        grand_total = (order.cgst * 2) + order.total_price
        context = {'order': order, 'tax': tax * 100,'main_order':main_order,'grand_total':grand_total}
    else:
        context ={}
    # Rendered
    html_string = render_to_string('genesis/order/pdf_ordered_items.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf(
        stylesheets=[
            # Change this to suit your css path
            str(settings.BASE_DIR) + '/static/order/css/main.css',
        ],)

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=' + \
        str(order.invoice_id)+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    # return render(request,'genesis/order/pdf.html')
    return response

@login_required(login_url="user_login")
def generate_invoice(request, id):
    # Generate PDF
    # Model data
    # Not for billing
    order = Order.objects.get(id=id, created_by=request.user.id)
    total = 0
    for obj in order.item_details.all():
        total = int(total) + int(obj.purchase_price_per_quantity) * \
            int(obj.quantity)
    tax = 0.18  # 18% default
    gst = tax * total
    grand_total = total + gst
    context = {'order': order, 'total': total, 'tax': tax *
               100, 'grand_total': grand_total, 'gst': gst}
    # Rendered
    html_string = render_to_string('genesis/order/pdf_full.html', context)
    html = HTML(string=html_string)
    result = html.write_pdf(
        stylesheets=[
            # Change this to suit your css path
            str(settings.BASE_DIR) + '/static/order/css/main.css',
        ],)

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=' + \
        str(order.number)+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    # return render(request,'genesis/order/pdf.html')
    return response


@login_required(login_url="user_login")
def dashboard(request):
    # speed up using a separate table in future
    context={}
    try:
        address = Address.objects.filter(created_by=request.user.id).count()
        inventory = Inventory.objects.filter(created_by=request.user.id).count()
        public_listing = Listing.objects.filter(
            created_by=request.user.id, status='PUBLIC').count()
        private_listing = Listing.objects.filter(
            created_by=request.user.id, status='PRIVATE').count()
        my_inventories = Inventory.objects.filter(created_by=request.user.id)
        my_list = []
        for obj in my_inventories:
            my_list.append(obj.id)
        placed = OrderedItems.objects.filter(
            inventory_name__in=my_list, order_status='PLACED').count()
        packed = OrderedItems.objects.filter(
            inventory_name__in=my_list, order_status='PACKED').count()
        shipped = OrderedItems.objects.filter(
            inventory_name__in=my_list, order_status='SHIPPED').count()
        rejected = OrderedItems.objects.filter(
            inventory_name__in=my_list, order_status='REJECTED').count()
        completed = OrderedItems.objects.filter(
            inventory_name__in=my_list, order_status='COMPLETED').count()

        context = {'address': address, 'inventory': inventory, 'public_listing': public_listing,
                'private_listing': private_listing, 'placed': placed, 'packed': packed, 'shipped': shipped, 'rejected': rejected, 'completed': completed}
    except Exception as e:
        messages.error(request, str(e))
    return render(request, 'genesis/dashboard.html', context)

# Start Address Views


def make_others_non_default(userid, id):
    try:
        address = Address.objects.filter(~Q(id=id), created_by=userid)
    except Exception as e:
        return False
    for obj in address:
        obj.is_default = False
        obj.save()
    return True


@login_required(login_url="user_login")
def show_all_address(request):
    address = Address.objects.filter(created_by=request.user.id)
    return render(request, 'genesis/address/show.html', {'address': address})


@login_required(login_url="user_login")
def add_new_address(request):
    if request.method == "POST":
        data = request.POST.copy()
        data['created_by'] = request.user.id
        if request.POST.get('is_default'):
            make_others_non_default(request.user.id, 0)
        form = AddressForm(data)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Address added Succesfully')
                return redirect('show_all_address')
            except Exception as e:
                messages.error(request, str(e))
                return redirect('show_all_address')
    else:
        form = AddressForm()
    return render(request, 'genesis/address/add.html', {'form': form})


@login_required(login_url="user_login")
def destroy_address(request, id):
    if request.method == "POST":
        try:
            address = Address.objects.filter(id=id, created_by=request.user.id).first()
            address.delete()
            messages.success(request, 'Item removed from address')
        except Exception as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "Unauthorized Request!")            
    return redirect("show_all_address")


@login_required(login_url="user_login")
def edit_address(request, id):
    try:
        address = Address.objects.filter(id=id, created_by=request.user.id).first()
        form = AddressForm(instance=address)
        context = {'form': form, 'edit_id': id}
    except Exception as e:
        messages.error(request, str(e))
        return redirect("show_all_address")
    return render(request, 'genesis/address/edit.html', context)


@login_required(login_url="user_login")
def update_address(request, id):
    try:
        address = Address.objects.filter(id=id, created_by=request.user.id).first()
        form = AddressForm(request.POST, instance=address)
        if request.POST.get('is_default'):
            make_others_non_default(request.user.id, id)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Address Updated Succesfully')
                return redirect("show_all_address")
            except Exception as e:
                messages.error(request, str(e))
                return redirect('show_all_address')
        return render(request, 'genesis/address/edit.html', {'address': address})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('show_all_address')

# End Address Views

# Start Inventory Views


@login_required(login_url="user_login")
def show_all_inventory(request):
    inventory = Inventory.objects.filter(created_by=request.user.id)
    return render(request, 'genesis/inventory/show.html', {'inventory': inventory})


@login_required(login_url="user_login")
def add_new_inventory(request):
    if request.method == "POST":
        data = request.POST.copy()
        data['created_by'] = request.user.id
        form = InventoryForm(data, user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Inventory added Succesfully')
                return redirect('show_all_inventory')
            except Exception as e:
                messages.error(request, str(e))
                return redirect('show_all_inventory')
    else:
        form = InventoryForm(user=request.user)
    return render(request, 'genesis/inventory/add.html', {'form': form})


@login_required(login_url="user_login")
def destroy_inventory(request, id):
    if request.method == "POST":
        try:
            inventory = Inventory.objects.filter(
                id=id, created_by=request.user.id).first()
            inventory.delete()
            messages.success(request, 'Item removed from inventory!')
        except Exception as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "Unauthorized Request!")
    return redirect("show_all_inventory")


@login_required(login_url="user_login")
def edit_inventory(request, id):
    try:
        inventory = Inventory.objects.filter(
            id=id, created_by=request.user.id).first()
        form = InventoryForm(instance=inventory, user=request.user)
        context = {'form': form, 'edit_id': id}
    except Exception as e:
        messages.error(request, str(e))
        return redirect('show_all_inventory')
    return render(request, 'genesis/inventory/edit.html', context)


@login_required(login_url="user_login")
def update_inventory(request, id):
    try:
        inventory = Inventory.objects.filter(
            id=id, created_by=request.user.id).first()
        form = InventoryForm(request.POST, instance=inventory, user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Inventory Updated Succesfully')
                return redirect("show_all_inventory")
            except Exception as e:
                messages.error(request, str(e))
                return redirect('show_all_inventory')
        return render(request, 'genesis/inventory/edit.html', {'inventory': inventory})
    except Exception as e:
        messages.error(request, str(e))
        return redirect('show_all_inventory')

# End Inventory Views

# Start Listing Views


@login_required(login_url="user_login")
def show_all_listing(request):
    listing = Listing.objects.filter(created_by=request.user.id)
    return render(request, 'genesis/listing/show.html', {'listing': listing})


@login_required(login_url="user_login")
def add_new_listing(request):
    if request.method == "POST":
        data = request.POST.copy()
        data['created_by'] = request.user.id
        form = ListingForm(data,request.FILES,user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Listing added Succesfully')
                return redirect('show_all_listing')
            except Exception as e:
                messages.error(request, str(e))
                return redirect('show_all_listing')
    else:
        form = ListingForm(user=request.user)
    return render(request, 'genesis/listing/add.html', {'form': form})


@login_required(login_url="user_login")
def destroy_listing(request, id):
    if request.method == "POST":
        try:
            listing = Listing.objects.filter(id=id, created_by=request.user.id).first()
            listing.delete()
            messages.success(request, 'Item removed from listing!')
        except Exception as e:
            messages.error(request, str(e))
    else:
        messages.error(request, "Unauthorized Request!")
    return redirect("show_all_listing")


@login_required(login_url="user_login")
def edit_listing(request, id):
    try:
        listing = Listing.objects.filter(id=id, created_by=request.user.id).first()
        form = ListingForm(instance=listing, user=request.user)
        context = {'form': form, 'edit_id': id}
    except Exception as e:
        messages.error(request, str(e))
        return redirect('show_all_listing')
    return render(request, 'genesis/listing/edit.html', context)


@login_required(login_url="user_login")
def update_listing(request, id):
    try:
        listing = Listing.objects.filter(id=id, created_by=request.user.id).first()
        form = ListingForm(request.POST,request.FILES,instance=listing, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing Update Successful")
            return redirect("show_all_listing")
    except Exception as e:
        messages.error(request, str(e))
        return redirect('show_all_listing')
    return render(request, 'genesis/listing/show.html', {'listing': listing})

# End Listing Views

# Start Order Views
# The orders are created in shoppingcart/views.py place_order()


@login_required(login_url="user_login")
def show_all_order(request):
    #query = request.GET.get('search')
    try:
        item = Order.objects.prefetch_related("item_details","item_details__item_name","item_details__inventory_name","item_details__weight_group").filter(
            created_by=request.user.id).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(item, 10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context = {'items': items}
        return render(request, 'genesis/order/show.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('dashboard')


@login_required(login_url="user_login")
def show_my_customer_orders(request):
    try:
        my_inventories = Inventory.objects.filter(created_by=request.user.id)
        my_list = []
        for obj in my_inventories:
            my_list.append(obj.id)
        item = OrderedItems.objects.filter(
            inventory_name__in=my_list).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(item, 10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context = {'items': items, 'item': item}
        return render(request, 'genesis/order/cusshow.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('dashboard')


@login_required(login_url="user_login")
def change_order_status(request, id):
    if request.method == 'POST':
        try:
            my_inventories = Inventory.objects.filter(created_by=request.user.id)
            my_list = []
            for obj in my_inventories:
                my_list.append(obj.id)
            # check if right id is sent
            ordereditem = OrderedItems.objects.filter(
                inventory_name__in=my_list, id=id).first()
            if ordereditem:
                ordereditem.order_status = request.POST.get('order_status')
                ordereditem.save()
            return redirect('show_my_customer_orders')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('show_my_customer_orders')

# End Order Views
# Start Quote
@login_required(login_url="user_login")
def add_new_quote(request):
    if request.method == "POST":
        data = request.POST.copy()
        data['created_by'] = request.user.id
        data['seller_action_required'] = True
        data['status'] = 'RECEIVED'
        form = QuoteForm(data,user=request.user)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Quote added Succesfully')
                # Seller Email Start
                app_name = settings.APP_NAME
                app_about = settings.APP_ABOUT
                listing = Listing.objects.get(id=data['item_name'])
                weight = Weight.objects.get(id=data['weight_group'])
                quantity = data['quantity']
                subject = "New Quote Request Received"
                message = f'Congratulations on receiving a new quote request for [{listing.name}] of quantity [{quantity} {weight.name}]. Check the panel to update your quote now!'
                context = {'app_about': app_about, 'message': message,
                        'subject': subject, 'app_name': app_name, 'user': listing.created_by.username}
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [listing.created_by.email, ]
                send_notification_email_task.delay(
                    context, email_from, recipient_list, subject)
                # Seller Email Stop
                # Customer Email Start
                subject = "New Quote Request Sent"
                message = f'Congratulations on sending a new quote request for [{listing.name}] of quantity [{quantity} {weight.name}]. We will notify you once a quote is generated!'
                context = {'app_about': app_about, 'message': message,
                        'subject': subject, 'app_name': app_name, 'user': request.user.username}
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [request.user.email, ]
                send_notification_email_task.delay(
                    context, email_from, recipient_list, subject)
                # Customer Email Stop
                return redirect('show_all_sent_quote')
            except Exception as e:
                messages.error(request, str(e))
                return redirect('show_all_sent_quote')
    else:
        pass

@login_required(login_url="user_login")
def show_all_sent_quote(request):
    try:
        quote = Quote.objects.select_related("item_name","weight_group","billing_address").filter(created_by=request.user.id)
        page = request.GET.get('page', 1)
        paginator = Paginator(quote, 10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context = {'items': items}
        return render(request, 'genesis/quote/sent.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('dashboard')

@login_required(login_url="user_login")
def show_all_received_quote(request):
    try:
        quote = Quote.objects.select_related("item_name","weight_group","billing_address").filter(item_name__created_by=request.user.id)
        page = request.GET.get('page', 1)
        paginator = Paginator(quote, 10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        context = {'items': items}
        return render(request, 'genesis/quote/received.html', context)
    except Exception as e:
        messages.error(request, str(e))
        return redirect('dashboard')

@login_required(login_url="user_login")
def edit_purchase_order(request, id):
    try:
        po = Quote.objects.filter(id=id, created_by=request.user.id).first()
        form = QuoteForm(instance=po, user=request.user)
        context = {'form': form, 'edit_id': id}
    except Exception as e:
        messages.error(request, str(e))
        return redirect('edit_purchase_order')
    return render(request, 'genesis/quote/edit_po_file.html', context)

@login_required(login_url="user_login")
def update_purchase_order(request, id):
    try:
        po = Quote.objects.filter(id=id, created_by=request.user.id).first()
        data = request.POST.copy()
        data_files = request.FILES
        data['item_name'] = po.item_name
        data['quantity'] = po.quantity
        data['weight_group'] = po.weight_group
        data['buyer_action_required'] = False
        data['seller_action_required'] = True
        data['status'] = 'PURCHASE_ORDER_SENT'
        # Check if order is completed before uploading
        if po.status == 'COMPLETED':
                messages.error(request, 'Upload no longer allowed!! Order status is completed!')
                return redirect('dashboard')
        form = QuoteForm(data,data_files,instance=po, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Purchase Order Update Successful")
            # Seller Email Start
            app_name = settings.APP_NAME
            app_about = settings.APP_ABOUT
            listing = Listing.objects.get(id=po.item_name.id)
            weight = Weight.objects.get(id=po.weight_group.id)
            quantity = data['quantity']
            subject = "New Purchase Order Received"
            message = f'Congratulations on receiving a new purchase order for [{listing.name}] of quantity [{quantity} {weight.name}]. Check the panel to update the invoice and delivery receipt now!'
            context = {'app_about': app_about, 'message': message,
                    'subject': subject, 'app_name': app_name, 'user': listing.created_by.username}
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [listing.created_by.email, ]
            send_notification_email_task.delay(
                context, email_from, recipient_list, subject)
            # Seller Email Stop
            # Customer Email Start
            subject = "New Purchase Order Sent"
            message = f'Congratulations on sending a new purchase order for [{listing.name}] of quantity [{quantity} {weight.name}]. We will notify you once the invoice and delivery receipt is generated!'
            context = {'app_about': app_about, 'message': message,
                    'subject': subject, 'app_name': app_name, 'user': po.created_by.username}
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [po.created_by.email, ]
            send_notification_email_task.delay(
                context, email_from, recipient_list, subject)
            # Customer Email Stop
            return redirect("show_all_sent_quote")
    except Exception as e:
        messages.error(request, str(e))
        return redirect('show_all_sent_quote')
    messages.error(request, str(form.errors))
    return redirect('dashboard')

@login_required(login_url="user_login")
def edit_quote_order(request, id):
    try:
        po = Quote.objects.filter(id=id, item_name__created_by=request.user.id).first()
        form = QuoteForm(instance=po, user=request.user)
        context = {'form': form, 'edit_id': id}
    except Exception as e:
        messages.error(request, str(e))
        return redirect('edit_quote_order')
    return render(request, 'genesis/quote/edit_quote_file.html', context)

@login_required(login_url="user_login")
def update_quote_order(request, id):
    try:
        po = Quote.objects.filter(id=id, item_name__created_by=request.user.id).first()
        data = request.POST.copy()
        data_files = request.FILES
        data['item_name'] = po.item_name
        data['quantity'] = po.quantity
        data['weight_group'] = po.weight_group
        data['buyer_action_required'] = True
        data['seller_action_required'] = False
        data['status'] = 'QUOTE_SENT'
        # Check if order is completed before uploading
        if po.status == 'COMPLETED':
                messages.error(request, 'Upload no longer allowed!! Order status is completed!')
                return redirect('dashboard')
        form = QuoteForm(data,data_files,instance=po, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Quote Update Successful")
            # Seller Email Start
            app_name = settings.APP_NAME
            app_about = settings.APP_ABOUT
            listing = Listing.objects.get(id=po.item_name.id)
            weight = Weight.objects.get(id=po.weight_group.id)
            quantity = data['quantity']
            subject = "New Quote Sent"
            message = f'Congratulations on sending a new quote for [{listing.name}] of quantity [{quantity} {weight.name}]. We will notify you once the purchase order is generated!Check the panel to update the invoice and delivery receipt now!'
            context = {'app_about': app_about, 'message': message,
                    'subject': subject, 'app_name': app_name, 'user': listing.created_by.username}
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [listing.created_by.email, ]
            send_notification_email_task.delay(
                context, email_from, recipient_list, subject)
            # Seller Email Stop
            # Customer Email Start
            subject = "New Quote Received"
            message = f'Congratulations on receiving a new quote for [{listing.name}] of quantity [{quantity} {weight.name}]. Check the panel to update the purchase order now!'
            context = {'app_about': app_about, 'message': message,
                    'subject': subject, 'app_name': app_name, 'user': po.created_by.username}
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [po.created_by.email, ]
            send_notification_email_task.delay(
                context, email_from, recipient_list, subject)
            # Customer Email Stop
            return redirect("show_all_received_quote")
    except Exception as e:
        messages.error(request, str(e))
        return redirect('show_all_received_quote')
    messages.error(request, str(form.errors))
    return redirect('dashboard')

@login_required(login_url="user_login")
def edit_dr_invoice(request, id):
    try:
        po = Quote.objects.filter(id=id, item_name__created_by=request.user.id).first()
        form = QuoteForm(instance=po, user=request.user)
        context = {'form': form, 'edit_id': id}
    except Exception as e:
        messages.error(request, str(e))
        return redirect('edit_dr_invoice')
    return render(request, 'genesis/quote/edit_dr_invoice_file.html', context)

@login_required(login_url="user_login")
def update_dr_invoice(request, id):
    try:
        po = Quote.objects.filter(id=id, item_name__created_by=request.user.id).first()
        data = request.POST.copy()
        data_files = request.FILES
        data['item_name'] = po.item_name
        data['quantity'] = po.quantity
        data['weight_group'] = po.weight_group
        data['buyer_action_required'] = False
        data['seller_action_required'] = False
        data['status'] = 'COMPLETED'
        # Check if order is completed before uploading
        if po.status == 'COMPLETED':
                messages.error(request, 'Upload no longer allowed!! Order status is completed!')
                return redirect('dashboard')
        form = QuoteForm(data,data_files,instance=po, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Invoice and Delivery Receipt Update Successful")
            # Seller Email Start
            app_name = settings.APP_NAME
            app_about = settings.APP_ABOUT
            listing = Listing.objects.get(id=po.item_name.id)
            weight = Weight.objects.get(id=po.weight_group.id)
            quantity = data['quantity']
            subject = "Order Completed"
            message = f'Congratulations on the completion of the order for [{listing.name}] of quantity [{quantity} {weight.name}]. No further action required!'
            context = {'app_about': app_about, 'message': message,
                    'subject': subject, 'app_name': app_name, 'user': listing.created_by.username}
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [listing.created_by.email, ]
            send_notification_email_task.delay(
                context, email_from, recipient_list, subject)
            # Seller Email Stop
            # Customer Email Start
            subject = "Order Invoice and Delivery Receipt sent"
            message = f'Congratulations on the completion of the order for [{listing.name}] of quantity [{quantity} {weight.name}]. Check the panel to view the invoice and delivery receipt!'
            context = {'app_about': app_about, 'message': message,
                    'subject': subject, 'app_name': app_name, 'user': po.created_by.username}
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [po.created_by.email, ]
            send_notification_email_task.delay(
                context, email_from, recipient_list, subject)
            # Customer Email Stop
            return redirect("show_all_received_quote")
    except Exception as e:
        messages.error(request, str(e))
        return redirect('show_all_received_quote')
    messages.error(request, str(form.errors))
    return redirect('dashboard')
# End Quote