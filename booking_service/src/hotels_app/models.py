from django.db import models


class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description
    

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
