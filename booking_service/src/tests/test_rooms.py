from rest_framework.test import APIClient
import pytest


client = APIClient()


@pytest.mark.django_db
def test_add_room_sucess(room_data):
    response = client.post('/rooms/add/', data=room_data)
    assert response.status_code == 201
    assert 'room_id' in response.data

@pytest.mark.django_db
def test_add_room_failure():
    response = client.post('/rooms/add/', data = {"description": "", "price":""})
    assert response.status_code == 400

@pytest.mark.django_db
def test_list_room_sorted(create_room):
    response = client.get('/rooms/?sort_by=price')
    assert response.status_code == 200
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_delete_room(create_room):
    response = client.delete(f'/rooms/delete/{create_room.pk}/')
    assert response.status_code == 204
