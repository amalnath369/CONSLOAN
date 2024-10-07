from django.db import models

class user_reg(models.Model):
    GENDERCHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=300,null=True)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=255)
    dob=models.DateField()
    gender = models.CharField(max_length=1, choices=GENDERCHOICES)