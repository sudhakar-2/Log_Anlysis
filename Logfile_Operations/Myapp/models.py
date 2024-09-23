from django.db import models

# Create your models here.
class Register(models.Model):
    Name=models.TextField()
    Email=models.EmailField()
    Password=models.TextField()

class User_Register(models.Model):
    Name=models.TextField()
    Email=models.EmailField()
    Password=models.TextField()

class Forgot_Password(models.Model):
    Name=models.TextField()
    Email=models.EmailField()
    DateTime=models.DateTimeField()
    OTP=models.TextField()
