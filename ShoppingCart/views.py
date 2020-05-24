from django.shortcuts import render
from django.http import HttpResponse
from shop.models import product, Categorydetail
from math import ceil


def index(request):
    allProds = []
    catprods = list(Categorydetail.objects.all().order_by('category_image'))
    n = len(catprods) - 4
    start_category = catprods[0], catprods[1]
    del catprods[:2]
    cat_length = len(catprods) - 1
    end_category = catprods[cat_length-1], catprods[cat_length]
    del catprods[cat_length-1:]
    middle_category = catprods
    no_slides = n//6 + ceil((n/6)-(n//6))
    allProds.append([list(start_category), middle_category, list(
        end_category), range(1, no_slides), no_slides])
    param = {'allProds': allProds}
    return render(request, 'index.html', param)


def viewCategory(request, categoryId):
    x = Categorydetail.objects.get(id=categoryId)
    prods = product.objects.filter(category_name_id=x)
    return render(request, 'viewCategory.html', {'prods': prods, 'categoryName': categoryId})
