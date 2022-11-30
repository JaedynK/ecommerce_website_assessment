from django.shortcuts import render, redirect
from .csv_data import csv_data
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from requests_oauthlib import OAuth1
from decouple import config
import math

products_interface = csv_data('./ecommerce_app/data/products.csv')
cart_interface = csv_data('./ecommerce_app/data/shopping_cart.csv')


def index(request):
    all_products = products_interface.all_data
    
    sizes = []
    s_count = 0
    m_count = 0
    l_count = 0
    
    for item in all_products:
        if s_count < 1:
            if item['category'] == 'small':
                s_count=+1
                sizes.append(item)
                
        if m_count < 1:
            if item['category'] == 'medium':
                sizes.append(item)
                m_count+=1

        if l_count < 1:
            if item['category'] == 'large':
                sizes.append(item)
                l_count+=1
    data = {
       "sizes" : sizes,
       
    }
    return render(request, 'index.html',data)

def category_list(request, category_name):
    all_products = products_interface.all_data

    category_items = []

    for item in all_products:
        #print(item['category'])
        if item['category'] == category_name:
            category_items.append(item)
    
    data = {
        'category_items' : category_items
    }
    return render(request, 'category.html', data)

def item_page(request, item_id):
    all_products = products_interface.all_data

    found_item = []
    for item in all_products:

        if item['id'] == str(item_id):
            item['name'] = item['name'].capitalize()
            found_item.append(item)
            data = {
                'item' : found_item
            }
            return render(request, 'item_page.html',data)
    else:
        return render(request, 'item_page.html')


def search_page(request):
    all_products = products_interface.all_data
    test_list = []
    
    if request.method == 'POST':
        searched = request.POST.get('searched')
        item_to_list = []
        for item in all_products:
            if str(searched).lower() == item['name']:
                item_to_list.append(item)
                return render(request, 'search_page.html',{"searched":item_to_list})
        else:
            try:
                key = config('key', default='')
                secrect_key = config('secrect_key', default='')
                auth = OAuth1(key, secrect_key)
                endpoint = f"http://api.thenounproject.com/icon/{searched}/"
                response = requests.get(endpoint, auth=auth)
                error_list = response.json()
                test_list.append(error_list['icon'])

                data = {
                    "out_of_stock" : test_list,
                    "searched" : searched
                }
                return render(request, 'error_page.html', data)
            except:
             
                error_message = 'And The Noun Project does not have any images of your search'
                data = {
                    "error" :  error_message,
                }
                return render(request, 'error_page.html',data)

def shopping_cart(request):
    
    all_cart = cart_interface.all_data
    cart_list = []
    total_cost = 0
    for items in all_cart:
        items['name'] = items['name'].capitalize()
        cart_list.append(items)
        total_cost += int(items['cost'])

    num = "{:,}".format(total_cost)

    data = {
        'list' : cart_list,
        'total_cost' : num,
    }
    
    return render(request, 'shopping_cart.html', data)

@csrf_exempt
def add_to_cart(request,item_id):
    all_products = products_interface.all_data
    all_cart = cart_interface.all_data

    if request.method == 'POST':
        if all_cart == []:
            for item in all_products:
                    if str(item_id) == item['id']:
                        item['quantity'] = 1
                        found_item = item
                        cart_interface.save_item_to_file(found_item)
                        return redirect('/shopping_cart')

        
        else:
            for item_in_cart in all_cart:
                if item_in_cart['id'] == str(item_id):

                    for delete in all_cart:
                        if delete['id'] == str(item_id):
                            print(delete)
                            cart_interface.remove_a_row(delete)
                            break

                    qty = int(item_in_cart['quantity'])
                    new_qty = qty + 1
                    item_in_cart['quantity'] = str(new_qty)

                    price = int(item_in_cart['cost'])
                    right_price = math.trunc((price/qty))
                    new_price = right_price + price
                    item_in_cart['cost'] = str(new_price)

                    print(item_in_cart)

                    found_item = item_in_cart
                    break

                else:
                    for item in all_products:
                        if str(item_id) == item['id']:
                            item['quantity'] = 1
                            found_item = item
                            break

            cart_interface.save_item_to_file(found_item)
            return redirect('/shopping_cart')

    
def remove_from_cart(request, item_id):
    all_cart = cart_interface.all_data

    for item_in_cart in all_cart:
        if item_in_cart['id'] == str(item_id):
            if item_in_cart['quantity'] == '1':
                for delete in all_cart:
                    if delete['id'] == str(item_id):
                        print(delete)
                        cart_interface.remove_a_row(delete)
                        break
            else:
                print('test')
                for delete in all_cart:
                    if delete['id'] == str(item_id):
                        cart_interface.remove_a_row(delete)
                        break

                qty = int(item_in_cart['quantity'])
                new_qty = qty - 1
                item_in_cart['quantity'] = str(new_qty)

                price = int(item_in_cart['cost'])
                right_price = math.trunc((price/qty))
                new_price = price - right_price
                item_in_cart['cost'] = str(new_price)

                print(item_in_cart)

                found_item = item_in_cart

                cart_interface.save_item_to_file(found_item)
    return redirect('/shopping_cart')
    

            