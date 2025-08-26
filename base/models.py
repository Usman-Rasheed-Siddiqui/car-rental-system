# The above code defines Django models for different types of cars with attributes like brand, model,
# description, price, availability, rental status, and image.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CAR_TYPE_CHOICES = [
    ('luxury', 'Luxury'),
    ('economy', 'Economy'),
    ('suv', 'SUV'),
    ('pickup', 'Pick Up'),
    ('other', 'Other'),
]

CARD_TYPE_CHOICES = {
    ('visa', 'VISA'),
    ('mastercard', 'Mastercard'),
}

class Car(models.Model):

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price_per_day = models.IntegerField()
    seats = models.IntegerField(default=5)
    fuel = models.CharField(max_length=15, default="petrol")
    image = models.ImageField(upload_to="media/")
    available = models.BooleanField(default=True)
    number_of_cars = models.IntegerField()

    rent_date = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES, default='economy')
         
    def __str__(self):
       return f"{self.brand} {self.model} - {'Available' if self.available else 'Not Available'}"

class User_info(models.Model):

    user = models.OneToOneField(User, on_delete= models.CASCADE)

    balance = models.IntegerField(default=0)
    card_number = models.IntegerField(blank=True, null=True)
    card_picture = models.FilePathField(path="static/card", recursive=True,  default="VISA_card.png")
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, default='visa')

    rented_car = models.IntegerField(default = 0)
    profile_picture = models.ImageField(upload_to="profile_pics/" , default = "profile_pics/default.jpg", null=True, blank=True)

    def __str__(self):
        return f'{self.user} info'

class History(models.Model):

    user = models.ForeignKey(User, on_delete= models.CASCADE)
    cars_rented = models.JSONField(default=list, blank=True, null=True)
    new_rented = models.JSONField(default=list, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user}'s history"
