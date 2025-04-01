from datetime import date, timedelta
from .test_rooms import client
import pytest


@pytest.mark.django_db
def test_add_booking_success(booking_data):
    response = client.post('/bookings/', data=booking_data)
    assert response.status_code == 201
    assert 'booking_id' in response.data

@pytest.mark.django_db
def test_add_booking_invalid_date(booking_data):
    booking_data["end_date"] = booking_data["start_date"] - timedelta(days=1)
    response = client.post('/bookings/', data=booking_data)
    assert response.status_code == 400
    assert "End date must be after start date" in str(response.data)

@pytest.mark.django_db
def test_add_booking_past_start_date(booking_data):
    booking_data["start_date"] = date.today() - timedelta(days=1)
    booking_data["end_date"] = date.today() + timedelta(days=1)
    response = client.post('/bookings/', data=booking_data)
    assert response.status_code == 400
    assert "Start date cannot be in the past" in str(response.data)

@pytest.mark.django_db
def test_list_booking_by_room(create_room, booking_data):
    client.post('/bookings/', data=booking_data)
    response = client.get(f'/bookings/room/{create_room.pk}/')
    assert response.status_code == 200
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_delete_booking(create_room, booking_data):
    response = client.post('/bookings/', data=booking_data)
    assert response.status_code == 201
    booking_id = response.data['booking_id']

    del_response = client.delete(f'/bookings/delete/{booking_id}/')
    assert del_response.status_code == 204
