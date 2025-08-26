from datetime import datetime, date

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import CustomUserCreationForm, CarForm, BalanceForm
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

            messages.success(request, 'Account created successfully. Please Login')
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
    
    if car_type == 'luxury':
        return redirect(f'/luxury/?rent_date={rent_date}&return_date={return_date}')
    
    if car_type == 'pickup':
        return redirect(f'/pickup/?rent_date={rent_date}&return_date={return_date}')

    if car_type == 'suv':
        return redirect(f'/suv/?rent_date={rent_date}&return_date={return_date}')

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

    # Get distinct brands
    brands = economy_cars.values_list("brand", flat=True).distinct()


    context = {'cars': economy_cars, 'economy_cars': economy_cars, 'rent_date': rent_date, 'return_date': return_date, "brands": brands}

    return render(request, 'base/car/economy.html', context)

def LuxuryCars(request):

    luxury_cars = Car.objects.filter(car_type='luxury', available=True)


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

    # Get distinct brands
    brands = luxury_cars.values_list("brand", flat=True).distinct()

    context = {'cars': luxury_cars, 'luxury_cars': luxury_cars, 'rent_date': rent_date, 'return_date': return_date, "brands":brands}

    return render(request, 'base/car/luxury.html', context)

def PickUpCars(request):

    pickup_cars = Car.objects.filter(car_type='pickup', available=True)


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

    # Get distinct brands
    brands = pickup_cars.values_list("brand", flat=True).distinct()

    context = {'cars': pickup_cars, 'pickup_cars': pickup_cars, 'rent_date': rent_date, 'return_date': return_date, "brands":brands}

    return render(request, 'base/car/pickup.html', context)

def SUVCars(request):

    suv_cars = Car.objects.filter(car_type='suv', available=True)


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

    # Get distinct brands
    brands = suv_cars.values_list("brand", flat=True).distinct()

    context = {'cars': suv_cars, 'suv_cars': suv_cars, 'rent_date': rent_date, 'return_date': return_date, "brands":brands}

    return render(request, 'base/car/suv.html', context)

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

                # History Saving
                history_user = History.objects.get(user=request.user)
                rental_history = history_user.cars_rented or []
                new_rent = []

                car_information = {"brand": car.brand, "model": car.model, "rent_date": rent_date, "return_date": return_date, "total_price": total_price, "image": car.image.url, "days": days, "id": car.id, "car_type": car.car_type, "price_per_day": car.price_per_day}
                rental_history.append(car_information)
                new_rent.append(car_information)

                history_user.cars_rented = rental_history
                history_user.new_rented = new_rent

                history_user.save()

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
    

    economy_cars = Car.objects.filter(car_type='economy', available=True)
    economy_brands = economy_cars.values_list("brand", flat=True).distinct() 

    luxury_cars = Car.objects.filter(car_type='luxury', available=True)
    luxury_brands = luxury_cars.values_list("brand", flat=True).distinct()

    suv_cars = Car.objects.filter(car_type='suv', available=True)
    suv_brands = suv_cars.values_list("brand", flat=True).distinct()

    pickup_cars = Car.objects.filter(car_type='pickup', available=True)
    pickup_brands = pickup_cars.values_list("brand", flat=True).distinct()


    histories = History.objects.select_related("user").all()

    user_form = CustomUserCreationForm(instance=user) 



    context = {'user_form': user_form, "user_info": user_info, "can_edit": can_edit, "user_object": user_object,

                "histories": histories,

                "economy_cars": economy_cars, "economy_brands": economy_brands,
                'luxury_cars': luxury_cars, "luxury_brands": luxury_brands, 
                'suv_cars': suv_cars, "suv_brands": suv_brands, 
                'pickup_cars': pickup_cars, "pickup_brands": pickup_brands,}
    
    return render(request, 'base/admin_page/front_admin.html', context)


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
                    messages.error(request, f"{error}")

            return render(request, 'base/admin_page/front_admin.html', {'form': form})

    else:
        form = CarForm()

    context = {"form": form}

    return render(request, 'base/admin_page/add_car.html', context)

@user_passes_test(admin_required, login_url = 'login' )
def AllRentalHistory(request):
    histories = History.objects.select_related("user").all()

    context = {"histories": histories}
    
    return render(request, "base/admin_page/rental_history.html", context)

@user_passes_test(admin_required, login_url = 'login' )
def CurrentRentals(request):
    histories = History.objects.select_related("user").all()

    count = 0
    for history in histories:
        if history.new_rented:
            count += 1

    context = {"histories": histories, "count": count}
    
    return render(request, "base/admin_page/current_rentals.html", context)

#--------------------------------------------------USER PROFILE-------------------------------------------------------------------

@login_required(login_url = 'login' )
def UserPanel(request):
    
    user_edit = request.GET.get("edit") == "1"
    user = request.user
    user_info = User_info.objects.get(user=user)
    history = History.objects.get(user=user)

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

        return redirect("user_profile")
    
    user_form = CustomUserCreationForm(instance=user)

    recent_rent = history.new_rented[-1] if history.new_rented else None

    context = {'form': user_form, "user_info": user_info, "user_edit": user_edit, "user_object": user_object, "recent_rent": recent_rent}
    return render(request, 'base/user_page/view_profile_user.html', context)

@login_required(login_url = 'login' )
def UserRentalHistory(request):
    histories = History.objects.get(user=request.user)

    count = len(histories.cars_rented)

    context = {"histories": histories, "count": count}
    
    return render(request, "base/user_page/user_rental_history.html", context)

@login_required(login_url = 'login' )
def UpdateBalance(request):

    user_info = User_info.objects.get(user=request.user)
    abs_balance = abs(user_info.balance)

    if request.method == "POST":
        form = BalanceForm(request.POST, request.FILES, instance=user_info)

        if form.is_valid():
            user_info = form.save(commit=False)   # don’t save yet
            user_info.user = request.user         # attach logged-in user
            user_info.save()
            messages.success(request, "Balance updated successfully")
            return redirect("update_balance")

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

            return render(request, 'base/user_page/update_balance.html', {'form': form, "user_info": user_info,})

    else:
        form = BalanceForm(instance=user_info)
    
    card_number = user_info.card_number
    card_number = str(card_number)

    four_letter = ""
    four = 0
    proper = []
    for num in card_number:
        four += 1
        four_letter += num
        if four == 4:
            proper.append(four_letter)
            four_letter = ""
            four = 0

    proper = " ".join(proper)
    
    context = {"form": form, "user_info": user_info, "proper": proper, "abs_balance": abs_balance}
    return render(request, "base/user_page/update_balance.html", context)

@login_required(login_url = 'login' )
def EditBalance(request):
    user_info = User_info.objects.get(user=request.user)
    
    if request.method == "POST":
        balance = request.POST.get("balance")
        card_number = request.POST.get("card_number")
        card_type = request.POST.get("card_type")

        card_type_change = False
        card_number_change = False
        balance_update = False

        if balance is not None:
            user_info.balance += int(balance)
            balance_update = True
        
        if card_number is not None and card_number != user_info.card_number:
            user_info.card_number = card_number
            card_number_change = True
        
        if card_type is not None and card_type != user_info.card_type:
            user_info.card_type = card_type
            user_info.card_picture = f"card/{card_type}_card.png"
            card_type_change = True


        user_info.save()

        # if card_number_change and card_type_change and balance_update:
        #     messages.success(request, "Balance updated and shifted to new card with updated number and type")    

        # elif card_number_change and balance_update:
        #     messages.success(request, "Balance updated and shifted to new card with updated number")

        # elif card_type_change and balance_update:
        #     messages.success(request, "Balance updated and shifted to new card with updated type")

        # elif card_number_change:
        #     messages.success(request, "Balance shifted to new card number")
        
        # elif card_type_change:
        #     messages.success(request, "Balance shifted to new card type")

        messages.success(request, "Balance/Card updated")

        return redirect("update_balance")

    context = {"user_info": user_info}
    return render(request, "base/user_page/pop_edit_balance.html", context)

#--------------------------------------------------RETURNING USER----------------------------------------------------------------

def returning(request):

    history = History.objects.get(user=request.user)

    recent_rent = None
    if history.new_rented:
        recent_rent = history.new_rented[-1]

    context = {"recent_rent": recent_rent}

    return render(request, "base/user_page/returning.html", context)

def confirm_return(request):
    history = History.objects.get(user=request.user)
    recent_rent = history.cars_rented[-1]
    user_info = User_info.objects.get(user=request.user)
    car = Car.objects.get(id=recent_rent["id"])
    

    if request.method == "POST":
        
        balance = user_info.balance

        balance = penalty(request, balance, history)
        balance = early_return(request, balance, history)

        rented_car = user_info.rented_car
        rented_car -= 1
        user_info.rented_car = rented_car
        user_info.balance = balance
        user_info.save()

        history.new_rented = []        
        history.save()

        no_of_cars = car.number_of_cars
        no_of_cars += 1
        car.number_of_cars = no_of_cars
        car.save()

        messages.success(request, "Car returned successfully")
        return redirect("home")

    
    context = {"recent_rent": recent_rent}

    return render(request, "base/user_page/returning.html", context)


def penalty(request, balance, history):

    cars_rented = history.cars_rented[-1]
    car_type = cars_rented["car_type"]

    today = date.today()

    return_date = cars_rented["return_date"]
    if isinstance(return_date, str):
        return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()
    else:
        return_date_obj = return_date

    if return_date_obj < today:
        days = (today - return_date_obj).days

        if car_type == "economy":
            penalty = 5000

        elif car_type == "luxury":
            penalty = 20000

        elif car_type == "suv":
            penalty = 10000
        
        elif car_type == "pickup":
            penalty = 15000

        extra_amount = days * penalty
        balance -= extra_amount
        
        cars_rented["return_date"] = today.strftime('%Y-%m-%d')
        history.cars_rented[-1] = cars_rented 
        history.save()


        messages.info(request, f"Return Date passed.\nPenalty: {extra_amount} PKR deducted from your balance.")    

    return balance

def early_return(request, balance, history):

    cars_rented = history.cars_rented[-1]
    price_per_day = int(cars_rented["price_per_day"])

    today = date.today()

    return_date = cars_rented["return_date"]
    if isinstance(return_date, str):
        return_date_obj = datetime.strptime(return_date, '%Y-%m-%d').date()
    else:
        return_date_obj = return_date


    if return_date_obj > today:
        days = (return_date_obj - today).days

        extra_amount = days * price_per_day
        balance += extra_amount
        
        cars_rented["return_date"] = today.strftime('%Y-%m-%d')
        history.cars_rented[-1] = cars_rented 
        history.save()

        messages.info(request, f"Early Return.\nDeposit: {extra_amount} PKR into your balance.")   

    return balance 
