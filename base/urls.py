
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
    path('find_car/', views.find_car, name="find_car"),
    path('renting/<int:pk>/', views.change_date, name="renting"),
    path('confirm-rent/<int:pk>/', views.confirm_rent, name="confirm-rent"),
    path('admin-panel/', views.AdminPanel, name="admin_panel"),
    path('economy-admin/', views.view_economy_car, name='economy_admin'), 
    path('view-car/<int:pk>/', views.view_car, name="view_car"),
    path('edit-car/<int:pk>/', views.edit_car, name="edit_car"),
    path('delete-car/<int:pk>/', views.DeleteCar, name="delete_car"),
    path('add-car/', views.AddCar, name="add_car")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)