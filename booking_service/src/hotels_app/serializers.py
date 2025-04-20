from rest_framework import serializers
from hotels_app.models import Room, Booking
from datetime import date
 


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Booking
        fields = '__all__'


    def validate(self, data):
        room = data.get('room_id')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if not Room.objects.filter(pk=room.room_id).exists():
            raise serializers.ValidationError("The room does not exitst")

        if start_date and end_date:    
            if end_date < start_date:
                raise serializers.ValidationError("End date must be after start date")
            if start_date < date.today():
                raise serializers.ValidationError("Start date cannot be in the past")
        
        return data    
