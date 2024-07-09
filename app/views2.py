from django.shortcuts import render
from .forms import Contactinfo
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import flight,passengers
from django.db.models import Q
import json
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from io import BytesIO

# Create your views here.
def home(request):
    return render(request, "index.html")


def book(request):
    if request.method == "POST":
        rdate = ""
        rday = ""
        date = request.POST["ddate"]
        origin = request.POST["origin"]
        destination = request.POST["destination"]
        date_object = datetime.strptime(date, "%Y-%m-%d")
        day_of_week = date_object.weekday()
        day_names = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        day = day_names[day_of_week]
        clas = request.POST["class"]
        if clas == "Economy":
            price_field = "economy_price"
        if clas == "Business":
            price_field = "bussiness_price"
        if clas == "First Class":
            price_field = "firstclass_price"

        if "return" in request.POST:
            rdate = request.POST["return"]
            date_object = datetime.strptime(date, "%Y-%m-%d")
            day_of_week = date_object.weekday()
            day_names = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
            rday = day_names[day_of_week]
        objects = flight.objects.filter(
            Q(origin__iexact=origin)
            & Q(destination__iexact=destination)
            & Q(day__iexact=day)
        ).values(
            "flight_id", "origin", "destination", "starttime", "endtime", price_field
        )
        objects = [x for x in objects if x[price_field] != 0]
        for obj in objects:
            obj["price"] = obj[price_field]

        return render(
            request,
            "book.html",  
            {
                "origin": origin,
                "destination": destination,
                "day": day,
                "date": date,
                "rday": rday,
                "rdate": rdate,
                "class": clas,
                "objects": objects,

            },
        )
    else:
        return render(request, "index.html")


# def services(request):
#     return render(request,'services.html')
def achievements(request):
    return render(request, "achievements.html")


def contact(request):
    return render(request, "contact-us.html")


def login(request):
    return render(request, "login.html")


def signup(request):
    return render(request, "signup.html")


def search_results(request):
    pass

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def contactinfo(request):
    if request.method == "POST":
       
       data = {
    'id': request.POST['flight_id'],
    'arrivaltime': request.POST['starttime'],
    'day': request.POST['day'],
    'date': request.POST['date'],
    'origin': request.POST['origin'],
    'departtime': request.POST['endtime'],
    'destination': request.POST['destination'],
     'clas' :request.POST["clas"],
    'price':request.POST['cost'],
    "form": Contactinfo
}

        
        
       return render(request, "contactinfo.html", data)
    else:
        return HttpResponseRedirect(reverse("home"))
def payment(request):
     
     totalpassengers=int(request.POST['totalpassengers'])
     passenger_list=[]
     for i in range(1,totalpassengers+1):
          passenger_name = request.POST.get(f"passenger_name{i}")
          passenger_age = request.POST.get(f"passenger_age{i}") 
          passenger_list.append({"name": passenger_name, "age": passenger_age})
        #   passengerobject= passengers.objects.create(name=passenger_name,age=int(passenger_age))  
        #   passengerobject.save()
     data = {
    'id': request.POST['flight_id'],
    'arrivaltime': request.POST['starttime'],
    'day': request.POST['day'],
    'date': request.POST['date'],
    'origin': request.POST['origin'],
    'departtime': request.POST['endtime'],
    'destination': request.POST['destination'],
      'clas' :request.POST["clas"],
#    'countrycode':request.POST["countrtycode"],
     'email':request.POST["email"],
     'phone':request.POST["phone"],
    'price':request.POST['cost'],
    "form": Contactinfo,
    'totalfare':request.POST['totalfare'],
    'price':request.POST['cost'],
    'totalpassengers':int(request.POST['totalpassengers']),
    'passengerlist':passenger_list
     }
   
   
     return render(request,"payment.html",data)

def gen_ticket(request):
     totalpassengers=int(request.POST['totalpassengers'])
     passenger_list=[]
     for i in range(1,totalpassengers+1):
          passenger_name = request.POST.get(f"passenger_name{i}")
          passenger_age = request.POST.get(f"passenger_age{i}") 
          passenger_list.append({"name": passenger_name, "age": passenger_age})
        #   passengerobject= passengers.objects.create(name=passenger_name,age=int(passenger_age))  
        #   passengerobject.save()
     data = {
    'id': request.POST['flight_id'],
    'arrivaltime': request.POST['starttime'],
    'day': request.POST['day'],
    'date': request.POST['date'],
    'origin': request.POST['origin'],
    'departtime': request.POST['endtime'],
    'destination': request.POST['destination'],
    'clas' :request.POST["clas"],
    'passengerlist':passenger_list,
    
    # 'countrycode':request.POST["countrtycode"],
    'email':request.POST["email"],
     'phone':request.POST["phone"],
    'price':request.POST['cost'],
    "form": Contactinfo,
    'totalfare':request.POST['totalfare'],
    'totalpassengers':int(request.POST['totalpassengers']),
    
    }
     
     return render(request,"gen_ticket.html",data)
def ticket(request):
    totalpassengers=int(request.POST['totalpassengers'])
    passenger_list=[]
    for i in range(1,totalpassengers+1):
          passenger_name = request.POST.get(f"passenger_name{i}")
          passenger_age = request.POST.get(f"passenger_age{i}") 
          passenger_list.append({"name": passenger_name, "age": passenger_age})
        #   passengerobject= passengers.objects.create(name=passenger_name,age=int(passenger_age))  
        #   passengerobject.save()
    data = {
    'id': request.POST['flight_id'],
    'arrivaltime': request.POST['starttime'],
    'day': request.POST['day'],
    'datee': request.POST['date'],
    'origin': request.POST['origin'],
    'departtime': request.POST['endtime'],
    'destination': request.POST['destination'],
    
    # 'countrycode':request.POST["countrtycode"],
     'email':request.POST["email"],
     'phone':request.POST["phone"],
    'price':request.POST['cost'],
    "form": Contactinfo,
    'clas' :request.POST["clas"],
    'totalfare':request.POST['totalfare'],
    'passengerlist':passenger_list,
   
    }
    # template_path = 'ticket.html'
    # template = get_template(template_path)
    # html = template.render(data)
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="ticket.pdf"'
    # pisa_status = pisa.CreatePDF(
    #     html, dest=response, link_callback=lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri))
    # if pisa_status.err:
    #     return HttpResponse('We had some errors <pre>' + html + '</pre>')
    # return response
    # pdf = render_to_pdf('ticket.html', data)
    # return HttpResponse(pdf, content_type='application/pdf')
    return render(request,"ticket.html",data)

from .forms import ContactForm
def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            # return redirect('success_page')  # Redirect to a success page
    else:
        form = ContactForm()
    
    return render(request, 'contact-us.html', {'form': form})


