from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class flight(models.Model):
    flight_id=models.CharField(max_length=100)
    origin=models.CharField(max_length=100)
    destination=models.CharField(max_length=100)
    starttime=models.TimeField(auto_now=False,auto_now_add=False)
    endtime=models.TimeField(auto_now=False,auto_now_add=False)
    economy_price=models.FloatField(max_length=100,null=True)
    bussiness_price=models.FloatField(max_length=100,null=True)
    firstclass_price=models.FloatField(max_length=100,null=True)
    day=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.flight_id}:{self.origin} to {self.destination}-{self.day}"
class passengers(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gender = models.CharField(max_length=10,null=True,default="Male")
    def __str__(self):
        return f"{self.name}:{self.age}-{self.gender}"
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name    
    

# class User(AbstractUser):
#     def __str__(self):
#         return f"{self.id}: {self.first_name} {self.last_name}"
TICKET_STATUS = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
]
import json   
class Ticket(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="bookings", blank=True, null=True)
    ref_no = models.CharField(max_length=6, unique=True)
    # passengers = models.ManyToManyField(passengers, related_name="flight_tickets")
    passengers = models.JSONField(blank=True, null=True) 
    flight = models.ForeignKey(flight, on_delete=models.CASCADE, related_name="tickets", blank=True, null=True)
    flight_ddate = models.DateField(blank=True, null=True)
    flight_adate = models.DateField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    flight_fare = models.FloatField(blank=True,null=True)
    other_charges = models.FloatField(blank=True,null=True)
    # coupon_used = models.CharField(max_length=15,blank=True)
    # coupon_discount = models.FloatField(default=0.0)
    total_fare = models.FloatField(blank=True, null=True)
    # seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    booking_date = models.DateTimeField(default=datetime.now)
    mobile = models.CharField(max_length=20,blank=True)
    email = models.EmailField(max_length=45, blank=True)
    status = models.CharField(max_length=45, choices=TICKET_STATUS)
    def get_passengers_list(self):
     return json.loads(self.passengers) if self.passengers else []

    # status = models.CharField(max_length=45, choices=TICKET_STATUS)
    def set_passengers(self, passengers):
        if isinstance(passengers, str):
            self.passengers = passengers
            print(1)
        else:
            self.passengers = json.dumps(passengers)
            print(0)

    def get_passengers(self):
        try:
            # Deserialize the JSON data to retrieve the list of passengers
            return json.loads(self.passengers) if self.passengers else []
        except json.JSONDecodeError:
            # Handle the case where the stored data is not a valid JSON string
            return []


    def __str__(self):
        return self.ref_no
    
    

    

    



