from django.shortcuts import render,redirect
from .forms import Contactinfo
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import flight,passengers,Ticket
from django.db.models import Q
import json,secrets
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    return render(request, "index.html")


def book(request):
    if request.method == "POST":
        if request.user.is_authenticated:
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
            return HttpResponseRedirect(reverse("login1"))
    else:
        return render(request, "index.html")


# def services(request):
#     return render(request,'services.html')
def achievements(request):
    return render(request, "achievements.html")


def contact(request):
    return render(request, "contact-us.html")


def login1(request):
    return render(request, "login.html")

def logoutpage(request):
    logout(request)
    return redirect('home')

def logged(request):
    
    if request.method=='POST':
        username=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
           return render(request, "login.html") 
        

    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, "login.html")

        

    
      


def signup(request):
    return render(request, "signup.html")
def register(request):
    if request.method=='POST':

        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['name']
        email=request.POST['email']
        
        password=request.POST['password']
        cnfpassword=request.POST['confirmPassword']
        if password != cnfpassword:
            return render(request, "signup.html", {
                "message": "Passwords must match."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            
            user.save()
        except:
            return render(request, "signup.html", {
                "message": "Username already taken."
            })
        # login(request, user)
        return HttpResponseRedirect(reverse("logged"))
    else:
        return render(request, "flight/register.html")


def search_results(request):
    pass


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
          passenger_gender = request.POST.get(f"passenger_gender{i}") 
          passenger_list.append({"name": passenger_name, "age": passenger_age,"gender": passenger_gender})
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
     
     id1 = request.POST['flight_id']
     arrivaltime = request.POST['starttime']
     day = request.POST['day']
     datee = request.POST['date']
     origin = request.POST['origin']
     departtime = request.POST['endtime']
     destination = request.POST['destination']
     email = request.POST['email']
     phone = request.POST['phone']
     price = request.POST['cost']
     clas = request.POST['clas']
     totalfare = request.POST['totalfare']

        
     flight1 = flight.objects.get(flight_id=id1 ,day=day)
   
     ticket= create_ticket(request.user,passenger_list,totalpassengers,flight1,datee,clas,totalfare,'91',email,phone)
     data['bid']=ticket.ref_no
     return render(request,"payment.html",data)
def gen_ticket(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            totalpassengers=int(request.POST['totalpassengers'])
            print(totalpassengers)
            passenger_list=[]
            for i in range(1,totalpassengers+1):
                passenger_name = request.POST.get(f"passenger_name{i}")
                passenger_age = request.POST.get(f"passenger_age{i}") 
                passenger_gender = request.POST.get(f"passenger_gender{i}") 
                passenger_list.append({"name": passenger_name, "age": passenger_age,"gender": passenger_gender})
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
            'bid':request.POST['bid'],
            
            
            }
            bid=(request.POST['bid'])
            ticket = Ticket.objects.get(ref_no=bid)
            ticket.status='Confirmed'
            ticket.save()
    
            return render(request,"gen_ticket.html",data)
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login1'))
def ticket(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            totalpassengers=int(request.POST['totalpassengers'])
            print(totalpassengers)
            passenger_list=[]
            for i in range(1,totalpassengers+1):
                passenger_name = request.POST.get(f"passenger_name{i}")
                passenger_age = request.POST.get(f"passenger_age{i}") 
                passenger_gender = request.POST.get(f"passenger_gender{i}") 
                
                passenger_list.append({"name": passenger_name, "age": passenger_age,"gender": passenger_gender})
                # passenger_list.append(passengers.objects.create(name=passenger_name,age=passenger_age))
                #   passengerobject= passengers.objects.create(name=passenger_name,age=int(passenger_age))  
                #   passengerobject.save()
            data = {
            'id1': request.POST['flight_id'],
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
            'totalpassengers':int(request.POST['totalpassengers']),
        
            }
            id1 = request.POST['flight_id']
            arrivaltime = request.POST['starttime']
            day = request.POST['day']
            datee = request.POST['date']
            origin = request.POST['origin']
            departtime = request.POST['endtime']
            destination = request.POST['destination']
            email = request.POST['email']
            phone = request.POST['phone']
            price = request.POST['cost']
            clas = request.POST['clas']
            bid = request.POST['bid']
            totalfare = request.POST['totalfare']

            
            # flight1 = flight.objects.get(flight_id=id1 ,day=day)
            print(passenger_list)
            print(datee)
            print(request.user)
            
            # ticket= create_ticket(request.user,passenger_list,totalpassengers,flight1,datee,clas,totalfare,'91',email,phone)
            # ticket.passengers.set_passengers(passengers)
            # retrieved_passengers = ticket.get_passengers()
            ticket = Ticket.objects.get(ref_no=bid)
            ticket.status='Confirmed'
            ticket.save()
            # print(retrieved_passengers)
            print(ticket.ref_no)
            print(ticket.flight.flight_id)
            print(ticket.status)
            data['ref_no'] = ticket.ref_no
            data['status'] = ticket.status
            data['booking_date'] = ticket.booking_date
            data['flight_id'] = ticket.flight.flight_id
             
            return render(request,"ticket.html",data)
        else:
            return HttpResponse("Method must be post.")
    else:
        return HttpResponseRedirect(reverse('login1'))

from .forms import ContactForm

def contact_us(request):
    if request.user.is_authenticated:
    
        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():
                form.save() 
                
        else:
            form = ContactForm()
        
        return render(request, 'contact-us.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('login1'))

# def create_ticket(user,passengers,passengerscount,flight1,flight_1date,clas,totalfare,countrycode,email,mobile):
    # ticket = Ticket.objects.create()
    # ticket.user = user
    # x= secrets.token_hex(3).upper()
    # print(x)
    # print(passengers)
    # ticket.ref_no = x
    # ticket.flight = flight1
    # # for passenger in passengers:
    # #     ticket.passengers.add(passenger)
    # # ticket.passengers.clear()
   
    # ticket.email = email
    # ticket.mobile = ('+'+countrycode+' '+mobile)   

    # # ticket.flight_ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]))
    # ticket.flight_ddate = datetime(2023, 11, 15)
    # ###################
    # # flight1ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
    # # flight1adate = (flight1ddate + flight1.duration)
    # ###################
    # # ticket.flight_adate = datetime(flight1adate.year,flight1adate.month,flight1adate.day)
    # ticket.total_fare=totalfare
    # ticket.other_charges=0
    # ticket.save()
    # ticket.passengers.set_passengers(passengers)
    # ticket.save()
   
    # return ticket
from datetime import datetime, timedelta
from django.utils import timezone
# def create_ticket(user, passengers, passengerscount, flight1, flight_1date, clas, totalfare, countrycode, email, mobile):
#         start_time = flight1.starttime() if callable(flight1.starttime) else flight1.starttime
#         end_time = flight1.endtime() if callable(flight1.endtime) else flight1.endtime

#         # Calculate duration as timedelta
#         duration = timedelta(hours=end_time.hour - start_time.hour, minutes=end_time.minute - start_time.minute)

#         # Calculate the date of arrival by adding the duration to the date of departure
#         date_of_arrival = flight_1date + duration

#         # Convert duration to a string for concatenation
#         duration_str = str(duration)
#         ticket = Ticket.objects.create(
#             user=user,
#             ref_no=secrets.token_hex(3).upper(),
#             flight=flight1,
#             email=email,
#             mobile='+' + countrycode + ' ' + mobile,
#             flight_ddate=flight_1date,
#             flight_adate=date_of_arrival,
#             flight_fare=totalfare,
#             total_fare=totalfare,
#             other_charges=0
#         )

#         # Save the ticket to the database
#         ticket.save()
#         print(passengers)
#         # Now, set the passengers for the ticket
#         ticket.set_passengers(passengers)
#         retrieved_passengers = ticket.get_passengers()
#         print(retrieved_passengers)


#         # Save the ticket again to update the passengers field
#         ticket.save()

#         return ticket

from datetime import timedelta
from django.utils import timezone
from .models import Ticket

from datetime import timedelta, datetime, time
from django.utils import timezone
from .models import Ticket
from datetime import timedelta, datetime
from django.utils import timezone
from .models import Ticket

from datetime import timedelta, datetime
from django.utils import timezone
from .models import Ticket

def create_ticket(user, passengers, passengerscount, flight1, flight_1date, clas, totalfare, countrycode, email, mobile):
    # Assuming starttime and endtime are datetime.time objects
    start_time = flight1.starttime
    end_time = flight1.endtime

    # Convert flight_1date to datetime.date object
    flight_1date = datetime.strptime(flight_1date, '%Y-%m-%d').date()

    # Convert flight_1date to datetime object for calculation
    departure_datetime = datetime.combine(flight_1date, start_time)

    # Calculate duration as timedelta
    duration = timedelta(hours=end_time.hour - start_time.hour, minutes=end_time.minute - start_time.minute)

    # Calculate the arrival datetime by adding the duration
    arrival_datetime = departure_datetime + duration

    # Extract date and time components
    date_of_arrival = arrival_datetime.date()
    time_of_arrival = arrival_datetime.time()

    # Set the duration field in the Ticket model
    duration_str = str(duration)
    print(duration_str)
    ticket = Ticket.objects.create(
        status='Pending',
        user=user,
        ref_no=secrets.token_hex(3).upper(),
        flight=flight1,
        email=email,
        mobile='+' + countrycode + ' ' + mobile,
        flight_ddate=flight_1date,
        flight_adate=date_of_arrival,
        duration=duration,  # Set the duration field
        flight_fare=totalfare,
        total_fare=int(totalfare)+200,
        other_charges=200,
        
    )

    # Save the ticket to the database
    ticket.save()

    # Now, set the passengers for the ticket
    ticket.set_passengers(passengers)
    

    # Save the ticket again to update the passengers field
    ticket.save()

    # Print the passengers after setting them on the ticket
    retrieved_passengers = ticket.get_passengers()
    print(retrieved_passengers)

    return ticket

    

from django.shortcuts import render, get_object_or_404
from .models import Ticket

def booki(request):
    if request.user.is_authenticated:
        # Retrieve tickets for the logged-in user
        tickets = Ticket.objects.filter(user=request.user)

        return render(request, 'booki.html', {'tickets': tickets})
    else:
        # Redirect to the login page if the user is not authenticated
        return HttpResponseRedirect(reverse('login'))
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})    
    



def download(request):
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
    'ref_no':request.POST['ref_no'],
    'booking_date':request.POST['booking_date'],
    'passengerlist':passenger_list,
   
    }
    data['final']=200+int(request.POST['totalfare'])
    # print(request.POST['datee'])
    pdf = render_to_pdf('1.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from io import BytesIO
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def cancel_ticket(request, ref_no):
    ticket = Ticket.objects.get(ref_no=ref_no)

    # Check if the ticket is already cancelled
    # if ticket.status == 'Cancelled':
    #     # Optionally, you can handle the case where the ticket is already cancelled
    #     return render(request, 'ticket_already_cancelled.html', {'ticket': ticket})

    # Update the ticket status to 'Cancelled'
    ticket.status = 'Cancelled'
    ticket.save()

    # Optionally, you can redirect to a success page or show a confirmation message
    return redirect('booki')
def flight_list(request):
    flights = flight.objects.all()
    return render(request, 'flight_list.html', {'flights': flights})

from .forms import FlightForm
def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flight_list')  # Redirect to a page displaying all flights
        else:
            return HttpResponse("invalid")
    else:
        form = FlightForm()

    # return render(request, 'add_flight.html')
    return render(request, 'add_flight.html', {'form': form})

def delete_flight(request, flight_id):
    flights = flight.objects.get(flight_id=flight_id)
    flights.delete()
    return redirect('flight_list')  # Redirect to a page displaying all flights


