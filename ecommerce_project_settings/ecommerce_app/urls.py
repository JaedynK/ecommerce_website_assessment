from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category_name>/', views.category_list, name='category_list'),
    path('item_page/<int:item_id>', views.item_page, name='item_page'),
    path('search_page/', views.search_page, name= "search_page"),#<str:search_name>
    path('shopping_cart/', views.shopping_cart, name= 'shopping_cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart')
]
