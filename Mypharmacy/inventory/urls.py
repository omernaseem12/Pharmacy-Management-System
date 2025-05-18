from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name = 'home'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('show_stock/', views.show_stock, name='show_stock'),
    path('order_history/<str:sort_by>', views.order_history, name='order_history'),
    path('order_history/', views.order_history, name='order_history'),
    path('edit/', views.edit, name='edit'),
    path('create_order/', views.create_order, name='create_order'),
    path('add_stock_fun/', views.add_stock_fun, name='add_stock_fun'),
    path('create_order_fun/', views.create_order_fun, name='create_order_fun'),
    path('order_del/<int:id>/', views.order_del, name='OrderDel'),
    path('order_change_status/<int:id>/', views.order_change_status, name='ChangeStatus'),
    path('order_change_status_single/<int:id>/', views.order_change_status_single, name='ChangeStatus_single'),
    path('show_stock/show_more/<int:id>/', views.show_more, name='show_more'),
    path('show_stock/show_more/re_stock/', views.re_stock, name='re_stock'),
    path('show_stock/search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('order_history/search_suggestions_order/', views.search_suggestions_order, name='search_suggestions_order'),
    path('order_history/order_single/<int:id>/', views.order_single, name='order_single'),


]

