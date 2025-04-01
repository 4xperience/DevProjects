import pytest
from hotels_app.models import Room
from datetime import date, timedelta


@pytest.fixture
def room_data():
    return{"description": "Nice view suite", "price": "200.00"}


@pytest.fixture
def create_room(db, room_data):
    return Room.objects.create(**room_data)


@pytest.fixture
def booking_data(create_room):
    today = date.today()
    return {
        "room_id": create_room.pk,
        "start_date": today + timedelta(days=1),
        "end_date": today + timedelta(days=3)
    }
