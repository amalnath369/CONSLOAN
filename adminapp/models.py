from django.db import models
from user1.models import *
# Create your models here.
class LAF(models.Model):
    EMPLOYEMENT=[
        ('salaried','Salaried'),
        ('self_employed','Self employed')
    ]
    profile=models.OneToOneField(user_reg,on_delete=models.CASCADE)
    employement_type=models.CharField(max_length=60,choices=EMPLOYEMENT)
    pannumber=models.CharField(max_length=10)
    panimage=models.FileField(upload_to='pan')
    incomeproof=models.FileField(upload_to='income')
    loanamount=models.BigIntegerField(null=True)
    empid=models.IntegerField(null=True)
class admini(models.Model):
    name=models.CharField(max_length=50)
    empid=models.PositiveIntegerField()
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=100)

class Loandisbursed(models.Model):
    profile=models.ForeignKey('LAF',on_delete=models.CASCADE)
    EMI=models.IntegerField(null=False)
    Dateofapproval=models.DateField(auto_now_add=True)

class Emipayment(models.Model):
    emi=models.ForeignKey(Loandisbursed,on_delete=models.CASCADE)
    paymentid=models.CharField(max_length=100,null=True,blank=True)
    amount=models.IntegerField()
    status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed'), ('Pending', 'Pending')], default='Pending')
    date=models.DateField(auto_now_add=True)
    No_of_Payments=models.IntegerField(default=0)

class employee(models.Model):
    GENDERCHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50,null=True)
    phone=models.IntegerField(null=True)
    dob=models.DateField(null=True)
    empid=models.PositiveIntegerField()
    email=models.EmailField(max_length=255)
    password=models.CharField(max_length=100)
    gender=models.CharField(max_length=1,choices=GENDERCHOICES,null=True)