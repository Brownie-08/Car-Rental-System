from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse , HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
# from xhtml2pdf import pisa
from django.template.loader import render_to_string
from .models import Car, Order, PrivateMsg
from .forms import CarForm, OrderForm, MessageForm



def home(request):
    context = {
        "title" : "Car Rental"
    }
    return render(request,'home.html', context)

def car_list(request):
    car = Car.objects.all()

    query = request.GET.get('q')
    if query:
        car = car.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query) |
            Q(like__icontains=query)
        )

    # pagination
    paginator = Paginator(car, 12)  # Show 12 cars per page
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        car = paginator.page(1)
    except EmptyPage:
        car = paginator.page(paginator.num_pages)

    context = {
        'car': car,
    }
    return render(request, 'car_list.html', context)




def car_detail(request, id=None):
    detail = get_object_or_404(Car,id=id)
    context = {
        "detail": detail
    }
    return render(request, 'car_detail.html', context)

def car_created(request):
    form = CarForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/")
    context = {
        "form" : form,
        "title": "Create Car"
    }
    return render(request, 'car_create.html', context)

@login_required
def car_update(request, id=None):
    detail = get_object_or_404(Car, id=id)
    form = CarForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Update Car"
    }
    return render(request, 'car_create.html', context)

@login_required
def car_delete(request,id=None):
    query = get_object_or_404(Car,id = id)
    query.delete()

    car = Car.objects.all()
    context = {
        'car': car,
    }
    return render(request, 'admin_index.html', context)

#order

@login_required
def order_list(request):
    order = Order.objects.all()

    query = request.GET.get('q')
    if query:
        order = order.filter(
            Q(movie_name__icontains=query)|
            Q(employee_name__icontains=query)
        )

    # pagination
    paginator = Paginator(order, 4)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        order = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        order = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        order = paginator.page(paginator.num_pages)
    context = {
        'order': order,
    }
    return render(request, 'order_list.html', context)

@login_required
def order_detail(request, id=None):
    detail = get_object_or_404(Order, id=id)
    context = {
        "detail": detail,
    }
    return render(request, 'order_detail.html', context) 

@login_required
def generate_receipt(request, id):
    detail = get_object_or_404(Order, id=id)
    user = request.user

    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()

    # Create a canvas object
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Draw text on the PDF
    p.drawString(100, height - 100, f"Order Id: {detail.id}")
    p.drawString(100, height - 120, f"Car Name: {detail.car_name}")
    p.drawString(100, height - 140, f"Dealer Name: {detail.dealer_name}")
    p.drawString(100, height - 160, f"Customer Name: {user.first_name} {user.last_name}")
    p.drawString(100, height - 180, f"Customer Email: {user.email}")
    p.drawString(100, height - 200, f"Customer Phone: {detail.cell_no}")
    p.drawString(100, height - 220, f"Address: {detail.address}")
    p.drawString(100, height - 240, f"From: {detail.date_from}")
    p.drawString(100, height - 260, f"To: {detail.date_to}")

    # Save the PDF file
    p.showPage()
    p.save()

    # Get PDF data from buffer
    pdf = buffer.getvalue()
    buffer.close()

    # Create HTTP response with PDF data
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{id}.pdf"'
    return response



@login_required
def order_created(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "form": form,
        "title": "Create Order"
    }
    return render(request, 'order_create.html', context)

@login_required
def order_update(request, id=None):
    detail = get_object_or_404(Order, id=id)
    form = OrderForm(request.POST or None, instance=detail)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
        "title": "Update Order"
    }
    return render(request, 'order_create.html', context)

@login_required
def order_delete(request,id=None):
    query = get_object_or_404(Order,id = id)
    query.delete()
    return HttpResponseRedirect("/listOrder/")

def newcar(request):
    new = Car.objects.order_by('-id')
    #seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query) |
            Q(like__icontains=query) 
        )

    # pagination
    paginator = Paginator(new, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'new_car.html', context)

def like_update(request, id=None):
    if request.method == 'POST':
        car = get_object_or_404(Car, id=id)
        car.like += 1
        car.save()
        return JsonResponse({'likes': car.like})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def popular_car(request):
    new = Car.objects.order_by('-like')
    # seach
    query = request.GET.get('q')
    if query:
        new = new.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query) |
            Q(like__icontains=query)   
        )

    # pagination
    paginator = Paginator(new, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        new = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        new = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        new = paginator.page(paginator.num_pages)
    context = {
        'car': new,
    }
    return render(request, 'new_car.html', context)

def contact(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect("/car/newcar/")
    context = {
        "form": form,
        "title": "Contact With Us",
    }
    return render(request,'contact.html', context)

#-----------------Admin Section-----------------
@login_required
def base_dash(request):
    return render(request, 'base_admin.html')

@login_required
def admin_car_list(request):
    car = Car.objects.order_by('-id')

    query = request.GET.get('q')
    if query:
        car = car.filter(
            Q(car_name__icontains=query) |
            Q(company_name__icontains=query) |
            Q(num_of_seats__icontains=query) |
            Q(cost_par_day__icontains=query) |
            Q(like__icontains=query) 
        )

    # pagination
    paginator = Paginator(car, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        car = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        car = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        car = paginator.page(paginator.num_pages)
    context = {
        'car': car,
    }
    return render(request, 'admin_index.html', context)

@login_required
def admin_msg(request):
    msg = PrivateMsg.objects.order_by('-id')
    context={
        "car": msg,
    }
    return render(request, 'admin_msg.html', context)


def msg_delete(request,id=None):
    query = get_object_or_404(PrivateMsg, id=id)
    query.delete()
    return HttpResponseRedirect("/message/")
