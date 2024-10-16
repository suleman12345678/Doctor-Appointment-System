from datetime import datetime
from django.db import models
from django.http import request
from django.contrib.auth.models import User

class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)



    def __str__(self):
        return self.first_name
    

    class Meta:
        ordering = ["-sent_date"]





class Doctors(models.Model):
    user_id = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    speciality = models.TextField() 
    Surgeons = models.TextField()
    Physician = models.TextField()
    Dentist = models.TextField()
    Gynaecologist = models.TextField()
    Dentist= models.TextField()
    Cardiologist = models.TextField()
