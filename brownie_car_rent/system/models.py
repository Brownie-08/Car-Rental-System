from django.db import models
from django.conf import settings
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


# Function to define the upload location for car images
def uploaded_location(instance, filename):
    return ("%s/%s") % (instance.car_name, filename)

# Model for Car
class Car(models.Model):
    image = models.ImageField(upload_to=uploaded_location, null=True, blank=True, width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    car_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    num_of_seats = models.IntegerField()
    cost_par_day = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField
    content = models.TextField()
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.car_name

    def get_absolute_url(self):
        return "/car/%s/" % (self.id)

# Model for Order
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    car_name = models.CharField(max_length=255)
    dealer_name = models.CharField(max_length=255)
    cell_no = models.CharField(max_length=15)
    address = models.TextField()
    date_from = models.DateField(default=timezone.now)
    date_to = models.DateField(default=timezone.now)

    def __str__(self):
        return self.car_name

    def get_absolute_url(self):
        return "/car/detail/%s/" % (self.id)

    def calculate_total_cost(self, cost_par_day):
        duration = (self.date_to - self.date_from).days + 1  # Including the end day
        return cost_par_day * duration

# Model for Private Messages
class PrivateMsg(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()