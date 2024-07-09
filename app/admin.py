from django.contrib import admin

# Register your models here.
from . models import flight
from . models import passengers,ContactMessage,Ticket

admin.site.register(flight)
admin.site.register(passengers)
admin.site.register(Ticket)
admin.site.register(ContactMessage)