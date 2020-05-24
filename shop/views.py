from django.shortcuts import render
from django.http import HttpResponse
from shop.models import product, contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.


def index(request):
    products = product.objects.all()
    allProds = []
    catprods = product.objects.values('category_name', 'id')
    cats = {item['category_name'] for item in catprods}
    for cat in cats:
        prod = product.objects.filter(category_name=cat)
        n = len(prod)
        no_slides = n//4 + ceil((n/4)-(n//4))
        allProds.append([prod, range(1, no_slides), no_slides])
    param = {'allProds': allProds}
    return render(request, 'shop/index.html', param)


def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in str(item.category_name).lower():
        return True
    else:
        return False


def recommendedProducts(cats):
    personalizeProd = []
    for cat in cats:
        prod = product.objects.filter(category_name=cat)
        n = len(prod)
        no_slides = n//4 + ceil((n/4)-(n//4))
        personalizeProd.append([prod, range(1, no_slides), no_slides])
    return personalizeProd


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = product.objects.values('category_name', 'id')
    cats = {item['category_name'] for item in catprods}
    for cat in cats:
        prodtemp = product.objects.filter(category_name=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        no_slides = n//4 + ceil((n/4) - (n//4))
        if len(prod) != 0:
            allProds.append([prod, range(1, no_slides), no_slides])

    recommendedProd = recommendedProducts(cats)
    params = {"allProds": allProds, 'errormsg': '', 'query': query}
    if len(allProds) == 0:
        params = {
            'errormsg': "Please make sure to enter relavent search query or use more general terms.", 'query': query, 'personalizedData': recommendedProd}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')


def Contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        Contacts = contact(name=name, email=email, phone=phone, desc=desc)
        Contacts.save()
        message = 'Your details has been submitted successfully. We will get back to you soon!'
        return render(request, 'shop/contact.html', {'msg': message})
    else:
        return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for items in update:
                    updates.append(
                        {'text': items.update_desc, 'time': items.timestamp})
                    response = json.dumps(
                        {"status": "success", "updates": updates, "itemsJson": order[0].item_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "noitem"}')
        except Exception as e:
            return HttpResponse('{"status": "error"}')
    return render(request, 'shop/tracker.html')


def productview(request, myid):
    prod = product.objects.filter(id=myid)
    return render(request, 'shop/prodview.html', {'product': prod[0]})


def checkout(request):
    if request.method == "POST":
        item_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + \
            " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Order(item_json=item_json, name=name, amount=amount, email=email, address=address,
                      city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed.")
        update.save()
        id = order.order_id
        message = 'Your order has been placed successfully. Thank you for ordering with us. Your order id is '
        return render(request, 'shop/checkout.html', {'id': id, 'name': name, 'msg': message})
    else:
        return render(request, 'shop/checkout.html')
