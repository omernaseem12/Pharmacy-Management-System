from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import Medicine,Order
from django.contrib import messages
from django.db.models import Q, F
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# Create your views here.

def home(request):
    today = date.today()
    three_months = today + relativedelta(months=3)
    exp_med_3 = Medicine.objects.filter(med_expiry__lte = three_months)
    len_3_mon = len(exp_med_3)
    exp_med = Medicine.objects.filter(med_expiry__lte = today)
    len_exp = len(exp_med)
    par_low = Medicine.objects.filter(med_par__gt= F('med_stock'))
    len_low = len(par_low)
    no_stock = Medicine.objects.filter(med_stock = 0)
    len_no_stock = len(no_stock)
    pending_orders = Order.objects.filter(order_status=False)
    len_pending = len(pending_orders)
    dic = {'exp_med_3':exp_med_3,'exp_med':exp_med,'par_low':par_low,
           'no_stock':no_stock,'pending_orders':pending_orders,
           'len_3_mon':len_3_mon,'len_exp':len_exp,'len_low':len_low,
           'len_no_stock':len_no_stock,'len_pending':len_pending}
    return render(request,'inventory/home.html',dic)

def add_stock(request):
    return render(request,'inventory/add_stock.html')

def add_stock_fun(request):
    if request.method == 'POST':
        brand = request.POST.get('brand','default').strip().upper()
        name = request.POST.get('name','default').strip().upper()
        batch = request.POST.get('batch','default')
        exp = request.POST.get('exp','default')
        dose = request.POST.get('dose','default')
        unit = request.POST.get('unit','default')
        par = request.POST.get('par','default')
        stock = request.POST.get('stock','default')
        unitprice = request.POST.get('unitprice','default')
        boxQ = request.POST.get('boxQ', 'default')
        dosageform = request.POST.get('dosageform','default').strip().upper()
        flag = request.POST.get('flag','default')
        if flag == 'on':
            flag = True
        else:
            flag = False

        #Checking if already exist
        if Medicine.objects.filter(med_brand=brand, med_name=name, med_dose = dose, med_dose_unit = unit).exists():
            messages.error(request, "Medicine with this brand and name already exists!")
            return redirect(add_stock)

        Medicine.objects.create(med_brand = brand,med_name = name,med_batch = batch, med_expiry = exp,med_dose = dose, med_dose_unit = unit ,med_par = par, med_stock = stock, med_unitprice = unitprice,med_boxprice= float(unitprice)*float(boxQ), med_boxQ = boxQ,med_dosage_form = dosageform,med_flag = flag)
        messages.error(request, "Successfully Added")
        return redirect('add_stock')

    return render(request,'inventory/add_stock.html')


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
                'batch': med.med_batch,
                'id':med.med_id,
                'form':med.med_dosage_form
            } for med in medicines
        ]
    return JsonResponse(results, safe=False)

def search_suggestions_order(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        orders = Order.objects.filter(
            (Q(order_name__icontains=query) |
            Q(order_brand__icontains=query) |
            Q(order_date__icontains=query))
        )[:10]  # Limit to top 10 results
        results = [
            {
                'name': ord.order_name,
                'brand': ord.order_brand,
                'date': ord.order_date,
                'id':ord.order_id,
                'form':ord.order_dosage_form,
                'dose':f'{ord.order_dose} {ord.order_dose_unit}'
            } for ord in orders
        ]
    return JsonResponse(results, safe=False)

def order_single(request,id):
    order = Order.objects.get(order_id=id)
    dic = {'order': order}
    return render(request, 'inventory/order_single.html', dic)



def show_stock(request):
    medicines = Medicine.objects.all()
    dic={'med':medicines}
    return render(request,'inventory/show_stock.html',dic)

def re_stock(request):
    selected_medicine = None

    if request.method == "POST" and 'select_btn' in request.POST:
        brand = request.POST.get('brand')
        name = request.POST.get('name')
        dose = request.POST.get('dose_sel', 'default')
        unit = request.POST.get('unit_sel', 0.0)
        dosage = request.POST.get('dosageform')

        try:
            selected_medicine = Medicine.objects.get(med_brand=brand, med_name=name, med_dose = dose, med_dose_unit = unit ,med_dosage_form=dosage)
        except Medicine.DoesNotExist:
            selected_medicine = None
            messages.error(request,"Medicine with this brand and name and dosage does not exists!")

    if request.method == 'POST' and 'update_btn' in request.POST:
        medicine_id = request.POST.get('medicine_id')
        medicine = Medicine.objects.get(med_id = medicine_id)
        medicine.med_brand = request.POST.get('brand', 'default').strip().upper()
        medicine.med_name = request.POST.get('name', 'default').strip().upper()
        medicine.med_batch = request.POST.get('batch', 'default')
        medicine.med_expiry = request.POST.get('exp', 'default')
        medicine.med_par = request.POST.get('par', 'default')
        medicine.med_stock = request.POST.get('stock', 'default')
        medicine.med_unitprice = request.POST.get('unitprice', 'default')
        medicine.med_boxQ = request.POST.get('boxQ', 'default')
        medicine.med_dosage_form = request.POST.get('dosageform', 'default').strip().upper()
        flag = request.POST.get('flag', 'default')
        if flag == 'on':
            flag = False
        else:
            flag = True
        medicine.med_flag = flag
        medicine.med_boxprice = float(medicine.med_unitprice)* float(medicine.med_boxQ)
        medicine.save()
        messages.error(request,"Successfully updated")
        return redirect('show_more', id=medicine_id)



    meds = Medicine.objects.all()
    med_brand = Medicine.objects.values('med_brand').distinct()
    med_name = Medicine.objects.values('med_name').distinct()
    dic = {'med':meds,'selected_medicine': selected_medicine,'med_brand':med_brand,'med_name':med_name}
    return render(request,'inventory/re_stock.html',dic)

def order_history(request, sort_by='order_status'):
    orders = Order.objects.all().order_by(sort_by)
    dic = {'order':orders}
    return render(request,'inventory/order_history.html',dic)

def show_more(request,id):
    med = Medicine.objects.get(med_id = id)
    dic = {'med':med}
    return render(request,'inventory/show_more.html',dic)


def edit(request):
    return HttpResponse('edit page')

def create_order(request):
    return render(request,'inventory/order.html')


def create_order_fun(request):
    if request.method == 'POST':
        brand = request.POST.get('brand','default').strip().upper()
        dose = request.POST.get('dose', 'default')
        unit = request.POST.get('unit', 'default')
        name = request.POST.get('name','default').strip().upper()
        stock = request.POST.get('stock','default')
        dosageform = request.POST.get('dosageform','default').strip().upper()

        #Checking if already exist
        if Order.objects.filter(order_brand=brand, order_name=name,order_dosage_form = dosageform, order_dose = dose, order_dose_unit = unit,order_status = False).exists():
            messages.error(request, "Order Already Exist (Running)")

        Order.objects.create(order_brand = brand,order_name = name,order_dose = dose, order_dose_unit = unit, order_stock = stock,order_dosage_form = dosageform)
        messages.error(request, "Order Successfully Placed")
        return redirect('order_history')

    return render(request,'inventory/order_history.html')


def order_del(request,id):
    try:
        order = Order.objects.get(order_id=id)
        order.delete()
    except Order.DoesNotExist:
        raise Http404("Todo not found")
    return redirect('order_history')

def order_change_status(request,id):
    order = Order.objects.get(order_id=id)
    status = order.order_status
    if status == True:
        status = False
    elif status == False:
        status = True
    order.order_status = status
    order.save()
    return redirect('order_history')

def order_change_status_single(request,id):
    order = Order.objects.get(order_id=id)
    status = order.order_status
    if status == True:
        status = False
    elif status == False:
        status = True
    order.order_status = status
    order.save()
    return redirect(f'/inventory/order_history/order_single/{id}')

def que(request):
    path = 'inventory/static/inventory/med_dummy_data.csv'
    with open(path, 'r') as file:
        lines = file.readlines()
    skip = []
    count = 0
    # Loop through data rows
    for line in lines[1:]:
        cols = line.strip().split(',')
        brand = cols[0].upper()
        name = cols[1].upper()
        batch = cols[2]
        dose = cols[3]
        dose_unit = cols[4]
        expiry = cols[5]
        par = cols[6]
        stock = cols[7]
        unit_price = cols[8]
        boxQ = cols[9]
        dosage_form = cols[10].upper()
        flag = cols[11]

        # Checking if already exist
        if Medicine.objects.filter(med_brand=brand, med_name=name, med_dose=dose, med_dose_unit=dose_unit).exists():
            skip.append(f'Medicine with Brand: {brand} - Name: {name} - dose: {dose} {dose_unit} already exist')
        else:
            Medicine.objects.create(med_brand=brand, med_name=name, med_batch=batch, med_expiry=expiry, med_dose=dose,
                                    med_dose_unit=dose_unit, med_par=par, med_stock=stock, med_unitprice=unit_price,
                                    med_boxprice=float(unit_price) * float(boxQ), med_boxQ=boxQ, med_dosage_form=dosage_form,
                                    med_flag=flag)
            count = count +1


    if skip == []:
        messages.error(request, "Successfully Added All Medicine")
        return redirect('show_stock')
    else:
        messages.error(request, f'Failed ')
        return redirect('show_stock')


