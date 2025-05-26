from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='pos_home'),
    path('returns/',views.refund, name='pos_return'),
    path('all_sales/',views.sales, name='pos_all_sales'),
    path('search_suggestions/', views.search_suggestions, name='search_suggestions'),
    path('all_sales/search_suggestions_sales/', views.search_suggestions_sales, name='search_suggestions_sales'),
    path('returns/search_suggestions_return/', views.search_suggestions_return, name='search_suggestions_return'),

    path('invoice/<int:order_id>/', views.generate_invoice_pdf, name='invoice-pdf'),
    path('returns/log/<int:id>/', views.return_log, name='return_log'),
    path('all_sales/show_more/<int:id>/', views.show_more_sale, name='show_more_sale'),
    path('create_sale/', views.create_sale, name='create_sale'),
    path('api/checkout/', views.create_order, name='create_order'),
    path('checkout/<int:order_id>/', views.checkout, name='checkout_page'),
    path('api/products/', views.product_list, name='product_list'),
]
