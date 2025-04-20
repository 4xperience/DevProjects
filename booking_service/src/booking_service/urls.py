"""
URL configuration for booking_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hotels_app import views

urlpatterns = [
    path('', views.api_root),

    # Room endpoints 
    path('rooms/', views.list_of_rooms, name='list_of_rooms'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),

    #Booking endpoint
    path('bookings/', views.add_booking, name='add_bookings'),
    path('bookings/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('bookings/room/<int:room_id>/', views.list_bookings_by_room, name='list_bookings_by_room')
]
