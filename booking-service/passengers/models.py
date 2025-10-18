from django.db import models
from bookings.models import Booking

class Passenger(models.Model):
    booking = models.ForeignKey(Booking, related_name='passengers', on_delete=models.CASCADE)
    title = models.CharField(max_length=3, choices=[('MR', 'Mr'), ('MS', 'Ms'), ('MRS', 'Mrs')])
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    passport_number = models.CharField(max_length=20)
    nationality = models.CharField(max_length=3)
    
    class Meta:
        db_table = 'passengers'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
