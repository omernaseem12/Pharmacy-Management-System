import datetime
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from inventory.models import Medicine, Order
from django.contrib import messages
from django.db.models import Q, F
from datetime import date, timedelta
from decimal import Decimal
import json
from .models import Order, OrderItem, Sale, Return

from django.template.loader import get_template
from weasyprint import HTML
from django.utils import timezone
import tempfile


today = date.today()
# Create your views here.



def home(request):
    invoice_url = request.session.pop('invoice_url', None)
    allsales = Sale.objects.order_by('-order_id')[:20]
    return render(request, 'pointofsale/home.html', {
        'invoice_url': invoice_url,'allsales':allsales,
    })


def refund(request):
    selected_data = None
    dic = {'selected_data': selected_data}
    if request.method == "POST" and 'date_btn' in request.POST:
        date = request.POST.get('date', '')
        print('DATE', date)
        if not date:
            date = None
            print('DATE', date)
        if date is not None:
            input_date = datetime.strptime(date, '%Y-%m-%d').date()
            print('DATE', input_date)
            if input_date > today:
                messages.error(request, f'Invalid Date Selection, Please Select Correct Date')
                return redirect(f'/pos/all_sales')
        if date != None:
            selected_data = Return.objects.filter(date=date)
            dic = {'selected_data': selected_data}
            return render(request, "pointofsale/returns.html", dic)
        else:
            selected_data = Return.objects.filter()
            dic = {'selected_data': selected_data}
            print(selected_data)
            return render(request, "pointofsale/returns.html", dic)
    return render(request, "pointofsale/returns.html", dic)

def return_log(request,id):
    orders = OrderItem.objects.filter(order_id = id)
    for order in orders:
        med = Medicine.objects.get(med_brand=order.brand, med_name=order.name, med_dose=order.unit, med_dose_unit=order.siunit, med_dosage_form = order.form)
        med.med_stock += int(order.quantity)
        med.save()
    Return.objects.create(order_id=id, date=today)
    return redirect('pos_return')

def sales(request):
    selected_data = None
    dic = {'selected_data': selected_data}
    if request.method == "POST" and 'select_btn' in request.POST:
        date = request.POST.get('date','')
        print('DATE',date)
        if not date:
            date = None
            print('DATE', date)
        if date is not None:
            input_date = datetime.strptime(date, '%Y-%m-%d').date()
            print('DATE', input_date)
            if input_date > today:
                messages.error(request,f'Invalid Date Selection, Please Select Correct Date')
                return redirect(f'/pos/all_sales')
        if date != None:
            selected_data = Sale.objects.filter(date = date)
            dic = {'selected_data':selected_data}
            return render(request,"pointofsale/all_sales.html",dic)
        else:
            selected_data = Sale.objects.filter()
            dic = {'selected_data': selected_data}
            print(selected_data)
            return render(request, "pointofsale/all_sales.html", dic)
    return render(request,"pointofsale/all_sales.html", dic)



def search_suggestions(request):

    query = request.GET.get('q', '')
    results = []
    if query:
        medicines = Medicine.objects.filter(
            (Q(med_name__icontains=query) |
            Q(med_brand__icontains=query) |
            Q(med_batch__icontains=query))
        )[:10]  # Limit to top 10 results
        results = [
            {
                'name': med.med_name,
                'brand': med.med_brand,
                'stock': med.med_stock,
                'id':med.med_id,
                'flag':med.med_flag,
                'dose':med.med_dose,
                'dose_unit':med.med_dose_unit,
                'form':med.med_dosage_form,
                'price':med.med_boxprice,
                'quantity':med.med_boxQ,
            } for med in medicines
        ]
    return JsonResponse(results, safe=False)

def search_suggestions_sales(request):

    query = request.GET.get('q', '')
    results = []
    if query:
        sales = Sale.objects.filter(
            (Q(customer_name__icontains=query) |
            Q(order_id__icontains=query) |
            Q(customer_phone__icontains=query))
        )  # Limit to top 10 results
        results = [
            {
                'name': sale.customer_name,
                'phone': sale.customer_phone,
                'grandtotal': sale.grandtotal,
                'id':sale.order_id,
            } for sale in sales
        ]
    return JsonResponse(results, safe=False)


def search_suggestions_return(request):

    query = request.GET.get('q', '')
    results = []
    if query:
        sales = Return.objects.filter(
            (Q(order_id__icontains=query))
        )  # Limit to top 10 results
        results = [
            {
                'id':sale.order_id,
                'date':sale.date
            } for sale in sales
        ]
    return JsonResponse(results, safe=False)

def show_more_sale(request,id):
    flag = False
    sale = Sale.objects.get(order_id = id)
    order = OrderItem.objects.filter(order_id=id)
    if Return.objects.filter(order_id=id):
        flag = True
    else:
        flag = False
    dic = {'sale':sale, 'order':order,'flag':flag}
    messages.error(request, f'Successfully Returned Order ID: {id}')
    return render(request, 'pointofsale/show_more_sale.html',dic)


def product_list(request):
    today = date.today()
    medicines = Medicine.objects.filter(med_stock__gt= 0, med_expiry__gt = today)
    data = [
        {
            'name': med.med_name,
                'brand': med.med_brand,
                'stock': med.med_stock,
                'id':med.med_id,
                'flag':med.med_flag,
                'dose':med.med_dose,
                'dose_unit':med.med_dose_unit,
                'form':med.med_dosage_form,
                'price':med.med_boxprice,
                'batch':med.med_batch,
                'quantity':med.med_boxQ,
        }
        for med in medicines
    ]
    return JsonResponse(data, safe=False)

def checkout(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()
    return render(request, 'pointofsale/checkout.html', {'order': order, 'items': items})




def create_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = data.get('cart', [])

        order = Order.objects.create()  # or include user/session info

        for item in cart:
            OrderItem.objects.create(
                order=order,
                name=item['name'],
                brand = item['brand'],
                form = item['form'],
                unit = item['dose'],
                siunit = item['dose_unit'],
                quantity=item['quantity'],
                price=item['price'],
                sub_total = float(item['quantity']) * float(item['price'])
            )

        return JsonResponse({'order_id': order.id})


def create_sale(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id','default')
        name = request.POST.get('name','default')
        phone = request.POST.get('phone','default')
        paid = request.POST.get('paid','default')
        payment_method = request.POST.get('payment_type','default')

    sum = 0
    tax = 0
    grandtotal = 0
    orders = OrderItem.objects.filter(order_id = order_id)
    for order in orders:
        med = Medicine.objects.get(med_brand=order.brand, med_name=order.name, med_dose=order.unit, med_dose_unit=order.siunit, med_dosage_form = order.form)
        if int(order.quantity) > med.med_stock:
            messages.error(request, f'Order quantity exceeds available stock.| {order.brand}-{order.name} Available: {med.med_stock}')
            return redirect(f'/pos/checkout/{order_id}')


    for order in orders:
        sum = sum + float(order.quantity)*float(order.price)

    tax = sum*0.1
    grandtotal = tax + sum
    returned = float(paid) - float(grandtotal)
    if float(paid) < grandtotal:
        messages.error(request, f'Paid Amount is Less Than Grand Total | {grandtotal}')
        return redirect(f'/pos/checkout/{order_id}')
    for order in orders:
        med = Medicine.objects.get(med_brand=order.brand, med_name=order.name, med_dose=order.unit,
                                   med_dose_unit=order.siunit, med_dosage_form=order.form)
        med.med_stock = int(med.med_stock) - int(order.quantity)
        med.save()

    Sale.objects.create(order_id = order_id,customer_name = name,customer_phone=phone,payment_type=payment_method,subtotal=sum,tax=tax,grandtotal=grandtotal,paid=paid,returned=returned)

    request.session['invoice_url'] = f"/pos/invoice/{order_id}/"
    request.session.save()
    return redirect('pos_home')



def generate_invoice_pdf(request, order_id):
    order = Sale.objects.get(order_id=order_id)
    order_items = OrderItem.objects.filter(order_id=order_id)

    # Render HTML template with context
    template = get_template('pointofsale/invoice_template.html')
    now = timezone.localtime()  # current datetime with timezone
    time_str = now.strftime('%I:%M %p')
    html_string = template.render({'order': order, 'today': timezone.localdate(), 'items':order_items,'time': time_str,'sub_total':order.subtotal,'tax':order.tax,'grandtotal':order.grandtotal,'payment_type':order.payment_type.upper(),'paid':order.paid,'returned':order.returned,'name':order.customer_name,'phone':order.customer_phone})

    # Generate PDF in memory
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="invoice.pdf"'

    # Convert HTML to PDF
    with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
        HTML(string=html_string).write_pdf(target=tmp_file.name)
        tmp_file.seek(0)
        response.write(tmp_file.read())

    return response

