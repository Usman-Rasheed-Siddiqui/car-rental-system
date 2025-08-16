from datetime import datetime

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, CarForm

from .models import Car, User_info, History
# Create your views here.

def home(request):

    request.session.pop('rent_date', None)
    request.session.pop('return_date', None)

    return render(request, 'base/home.html')


def loginPage(request):

    page = "login"


    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_object = User.objects.get(email=email)
            username = user_object.username     # Fetching username from User object

            user = authenticate(request, username= username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Login Successful, Welcome {username.title()}")
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')

        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')

    context = {'page': page}

    return render(request, 'base/login-register.html', context)


def registerPage(request):

    page = 'register'

    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            User_info.objects.create(user=user)
            History.objects.create(user=user)

            messages.success(request, 'Account created successfully')
            return redirect('login')
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    context = {'form': form, 'page': page}
    return render(request, 'base/login-register.html', context)


def logoutUser(request):

    logout(request)
    return redirect('home')


def find_car(request):
    car_type = request.GET.get('car_type')
    rent_date = request.GET.get('rent_date')
    return_date = request.GET.get('return_date')

    context = {'car_type': car_type, 'rent_date': rent_date, 'return_date': return_date}


    try:
        if not rent_date or not return_date:
            messages.error(request, "Please provide both rental and return dates.")
            return render(request, 'base/home.html', context)

        rental_date_proper = datetime.strptime(rent_date, '%Y-%m-%d').date()
        return_date_proper = datetime.strptime(return_date, '%Y-%m-%d').date()

        if rental_date_proper >= return_date_proper:
            messages.error(request, 'Return date must be after rental date')
            return render(request, 'base/home.html', context)

        if rental_date_proper < datetime.now().date():
            messages.error(request, "Rental date cannot be in past")
            return render(request, 'base/home.html', context)
            
    except ValueError:
        messages.error("Invalid date format")
        return render(request, 'base/home.html', context)


    request.session['rent_date'] = rent_date
    request.session['return_date'] = return_date

    if car_type == 'economy':
        return redirect(f'/economy/?rent_date={rent_date}&return_date={return_date}')

    else:
        return redirect('home')


def EconomyCars(request):

    economy_cars = Car.objects.filter(car_type='economy', available=True)


    rent_date = request.GET.get('rent_date')
    return_date = request.GET.get('return_date')

    if rent_date and return_date:
        try:
            rental_date_proper = datetime.strptime(rent_date, '%Y-%m-%d').date()
            return_date_proper = datetime.strptime(return_date, '%Y-%m-%d').date()

            if rental_date_proper >= return_date_proper:
                messages.error(request, 'Return date must be after rental date')
                return redirect("home")

            if rental_date_proper < datetime.now().date():
                messages.error(request, "Rental date cannot be in past")
                return redirect("home")
                
        except ValueError:
            messages.error("Invalid date format")
            return redirect('home')


    context = {'cars': economy_cars, 'economy_cars': economy_cars, 'rent_date': rent_date, 'return_date': return_date}

    return render(request, 'base/car/economy.html', context)

# ---------------------------------------------- Renting User-----------------------------------------------------------------

@login_required(login_url = 'login' )
def change_date(request, pk):
    car = Car.objects.get(id=pk)

    rent_date = request.GET.get('rent_date')
    return_date = request.GET.get('return_date')

    if rent_date:
        request.session['rent_date'] = rent_date
    else:
        rent_date = request.session.get('rent_date')

    if return_date:
        request.session['return_date'] = return_date
    else:
        return_date = request.session.get('return_date')

    days = None
    total_price = 0

    if rent_date and return_date:
        try:
            rental_date_obj = datetime.strptime(rent_date, '%Y-%m-%d').date()
            return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()

            if rental_date_obj >= return_date_obj:
                messages.error(request, 'Return date must be after rental date')
                return render(request, "base/renting.html", {
                    "car": car,
                    "rent_date": rent_date,
                    "return_date":return_date,
                    "days": None,
                    "total_price": None,
                })

            if rental_date_obj < datetime.now().date():
                messages.error(request, "Rental date cannot be in past")
                return render(request, "base/renting.html", {
                    "car": car,
                    "rent_date": rent_date,
                    "return_date":return_date,
                    "days": None,
                    "total_price": None,
                })
            
            days = (return_date_obj - rental_date_obj).days

            if days > 0:     
                total_price = car.price_per_day * days

        except ValueError:
            messages.error(request, "Invalid Dates")

    context = {"car": car, 'rent_date': rent_date, 'return_date': return_date, 'days': days, "total_price": total_price}
    return render(request, "base/renting.html", context)


@login_required(login_url = 'login' )
def confirm_rent(request, pk):

    car = Car.objects.get(id=pk)
    user_info = User_info.objects.get(user=request.user)

    rent_date = request.GET.get('rent_date') or request.session.get('rent_date')
    return_date = request.GET.get('return_date') or request.session.get('return_date')

    days = None
    total_price = 0
    
    if not rent_date or not return_date:
        messages.error(request, "Please Provide Appropriate Dates")
        return redirect("renting", pk=car.id)


    if rent_date and return_date:
        try:
            rent_date_obj = datetime.strptime(rent_date, '%Y-%m-%d').date()
            return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()


            days = (return_date_obj - rent_date_obj).days

        except ValueError:
            messages.error(request, "Invalid Dates")
            return redirect("renting", pk=car.id)


    if user_info.rented_car == 1:
        messages.error(request, "Only 1 Car can be rented")
        return redirect("renting", pk=car.id)

    if days is not None and days > 0: 
        try:
            
            total_price = car.price_per_day * days

            if user_info.balance < total_price:
                messages.error(request, "Balance Insufficient")
            
            elif not car.available:
                messages.error(request, "Car is Not Available")
            
            elif car.number_of_cars <= 0:
                messages.error(request, "No more cars available")
                
            else:
                user_info.balance -= total_price
                user_info.rented_car += 1
                user_info.save()

                car.number_of_cars -= 1
                if car.number_of_cars == 0:
                    car.available = False

                car.save()

                messages.success(request, "Car Rented Successfully")
        
        except ValueError:
            messages.error(request, "Balance Insufficient")

    request.session.pop('rent_date', None)
    request.session.pop('return_date', None)


    context = {"car": car, 'rent_date': rent_date, 'return_date': return_date, 'days': days, "total_price": total_price}  
    return render(request, "base/renting.html", context)


#  -------------------------------------------------- Admin Panel ------------------------------------------------------------

def admin_required(user):
    return user.is_superuser

@user_passes_test(admin_required, login_url = 'login' )
def AdminPanel(request):
    
    can_edit = request.GET.get("edit") == "1"
    user = request.user
    user_info = User_info.objects.get(user=user)

    user_object = User.objects.get(id = user.id)


    if request.method == 'POST':

        if 'profile_picture' in request.FILES:
            profile_picture = request.FILES['profile_picture']
            user_info.profile_picture = profile_picture
            user_info.save()

        first_name = request.POST.get('first_name')
        last_name = request.POST.get("last_name")

        if first_name is not None:
            user_object.first_name = first_name
        if last_name is not None:
            user_object.last_name = last_name

        user_object.save()

        return redirect("admin_panel")
    
    suzuki = Car.objects.filter(brand="Suzuki", available=True)
    toyota = Car.objects.filter(brand="Toyota", available=True)
    user_form = CustomUserCreationForm(instance=user)

    context = {'form': user_form, "user_info": user_info, "can_edit": can_edit, "user_object": user_object, "suzuki": suzuki, "toyota": toyota}
    return render(request, 'base/admin_page/front_admin.html', context)


@user_passes_test(admin_required, login_url = 'login' )
def view_economy_car(request):
    economy_cars = Car.objects.filter(car_type='economy', available=True)
    suzuki = economy_cars.filter(brand="Suzuki")
    toyota = economy_cars.filter(brand="Toyota")
    context = {'cars': economy_cars, 'economy_cars': economy_cars, "suzuki": suzuki, "toyota": toyota}

    return render(request, "base/admin_page/economy_admin.html", context)

@user_passes_test(admin_required, login_url = 'login' )
def view_car(request, pk):
    car = Car.objects.get(id=pk)
    context = {"car": car}
    return render(request, "base/admin_page/view_car.html", context)

@user_passes_test(admin_required, login_url = 'login' )
def edit_car(request, pk):

    car = Car.objects.get(id=pk)

    if request.method == "POST":
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        description = request.POST.get("description")
        seats = request.POST.get("seats")
        fuel = request.POST.get("fuel")
        price_per_day = request.POST.get("price_per_day")
        number_of_cars = request.POST.get("number_of_cars")
        available = request.POST.get("available")

        # For file uploads:
        image = request.FILES.get("image")

        if brand is not None:
            car.brand = brand

        if model is not None:
            car.model = model

        if description is not None:
            car.description = description

        if seats is not None:
            car.seats = seats

        if fuel is not None:
            car.fuel = fuel

        if price_per_day is not None:
            car.price_per_day = price_per_day

        if number_of_cars is not None:
            car.number_of_cars = number_of_cars

        if available is not None:
            car.available = available

        if image is not None:
            car.image = image

        car.save()

        return redirect("view_car", pk=car.id)

    context = {"car": car}
    return render(request, 'base/admin_page/pop_edit.html', context)

@user_passes_test(admin_required, login_url = 'login' )
def DeleteCar(request, pk):
    car = Car.objects.get(id=pk)

    if request.method == "POST":
        car.delete()
        messages.success(request, "Car Deleted Successfully")
        return redirect("admin_panel")

    context = {"car": car}
    return render(request, "base/admin_page/view_car.html", context)


@user_passes_test(admin_required, login_url = 'login' )
def AddCar(request):

    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Car Added Successfully")
            return redirect("admin_panel")
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

            return render(request, 'base/admin_page/front_admin.html', {'form': form})

    else:
        form = CarForm()

    context = {"form": form}

    return render(request, 'base/admin_page/add_car.html', context)

