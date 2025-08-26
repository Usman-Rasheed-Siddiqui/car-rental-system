
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path("logout/", views.logoutUser, name='logout'),

    path('economy/', views.EconomyCars, name='economy'),
    path('luxury/', views.LuxuryCars, name='luxury'),
    path('pickup/', views.PickUpCars, name='pickup'),
    path('suv/', views.SUVCars, name='suv'),

    path('find_car/', views.find_car, name="find_car"),
    path('renting/<int:pk>/', views.change_date, name="renting"),
    path('confirm-rent/<int:pk>/', views.confirm_rent, name="confirm-rent"),
    path('returning/', views.returning, name="returning"),
    path('confirm-return/', views.confirm_return, name="confirm_return"),


    path('admin-panel/', views.AdminPanel, name="admin_panel"),
    path('view-car/<int:pk>/', views.view_car, name="view_car"),
    path('edit-car/<int:pk>/', views.edit_car, name="edit_car"),
    path('delete-car/<int:pk>/', views.DeleteCar, name="delete_car"),
    path('add-car/', views.AddCar, name="add_car"),

    path('user-profile/', views.UserPanel, name="user_profile"),

    path("all-rental-histories", views.AllRentalHistory, name="all_rental_histories"),
    path("current-rentals", views.CurrentRentals, name="current_rentals"),
    path("user-rental-history", views.UserRentalHistory, name="user_rental_history"),

    path("update-balance", views.UpdateBalance, name="update_balance"),
    path("edit-balance", views.EditBalance, name="edit_balance"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)