from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from hotels_app.models import Room, Booking
from hotels_app.serializers import RoomSerializer, BookingSerializer
from django.db.models import QuerySet


@api_view(['GET'])
def api_root(request):
    return Response({'message': 'Welcome to the Hotel Booking API'})


# -------Room Views-------


@api_view(['POST'])
def add_room(request):
    serializer = RoomSerializer(data=request.data)
    if serializer.is_valid():
        room = serializer.save()
        return Response({'room_id': room.room_id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_of_rooms(request):
    sort_by = request.query_params.get('sort_by')

    valid_fields = ['price', 'add_date']
    if sort_by:
        raw_field = sort_by.lstrip('-')
        if raw_field not in valid_fields:
            return Response({'error': 'Invalid sort_by parameter'}, status=status.HTTP_400_BAD_REQUEST)

    rooms: QuerySet = Room.objects.all()
    if sort_by:
        rooms = rooms.order_by(sort_by)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_room(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    room.delete()
    return Response({'message': f'Room {room_id} and its bookings deleted'}, status=status.HTTP_204_NO_CONTENT)


# -------Booking Views-------


@api_view(['POST'])
def add_booking(request):
    serializer = BookingSerializer(data=request.data)
    if serializer.is_valid():
        booking = serializer.save()
        return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return Response({'message': f'Booking {booking_id} deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_bookings_by_room(request, room_id):
    bookings = Booking.objects.filter(room_id=room_id).order_by('start_date')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)
