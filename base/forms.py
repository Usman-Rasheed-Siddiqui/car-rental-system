
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Car


class CustomUserCreationForm(UserCreationForm):
    
    email = forms.EmailField(required=True, max_length=150)
    username = forms.CharField(required=True, max_length=150)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean(self):
        self.cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user
    
class CarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = '__all__'
    
    # ---- Field-level validation ----
    def clean_brand(self):
        brand = self.cleaned_data.get("brand")
        if not brand:
            raise forms.ValidationError("Brand is required.")
        if len(brand) < 2:
            raise forms.ValidationError("Brand name must be at least 2 characters.")
        return brand

    def clean_model(self):
        model = self.cleaned_data.get("model")
        if not model:
            raise forms.ValidationError("Model is required.")
        if len(model) < 1:
            raise forms.ValidationError("Model name cannot be empty.")
        return model

    def clean_price_per_day(self):
        price = self.cleaned_data.get("price_per_day")
        if price is None or price <= 0:
            raise forms.ValidationError("Price per day must be a positive number.")
        return price

    def clean_seats(self):
        seats = self.cleaned_data.get("seats")
        if seats is None or seats < 2:
            raise forms.ValidationError("There must be at least 2 seats.")
        if seats > 30:
            raise forms.ValidationError("Seats cannot exceed 30.")
        return seats

    def clean_fuel(self):
        fuel = self.cleaned_data.get("fuel")
        valid_fuels = ["petrol", "diesel", "electric", "hybrid"]
        if fuel.lower() not in valid_fuels:
            raise forms.ValidationError(f"Fuel type must be one of: {', '.join(valid_fuels)}.")
        return fuel

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise forms.ValidationError("Car image is required.")
        return image

    def clean_available(self):
        available = self.cleaned_data.get("available")
        # BooleanField is handled by Django, but you can enforce business rules
        return available

    def clean_number_of_cars(self):
        num = self.cleaned_data.get("number_of_cars")
        if num is None or num < 1:
            raise forms.ValidationError("There must be at least 1 car available.")
        return num

    def clean_car_type(self):
        car_type = self.cleaned_data.get("car_type")
        valid_choices = [choice[0] for choice in self._meta.model._meta.get_field("car_type").choices]
        if car_type not in valid_choices:
            raise forms.ValidationError("Invalid car type selected.")
        return car_type

    # ---- Form-wide validation ----
    def clean(self):
        cleaned_data = super().clean()

        price = cleaned_data.get("price_per_day")
        seats = cleaned_data.get("seats")

        # Example cross-field validation
        if price and seats:
            if price < 500 and seats > 7:
                raise forms.ValidationError(
                    "Large cars (more than 7 seats) must cost at least 500 per day."
                )

        return cleaned_data
