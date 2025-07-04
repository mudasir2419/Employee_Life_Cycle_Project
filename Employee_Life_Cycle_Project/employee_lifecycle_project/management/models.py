from django.db import models

class Department(models.Model):

    name = models.CharField(max_length=100, unique=True)  
    location = models.CharField(max_length=100,)

    def __str__(self):
        return self.name

class Employee(models.Model):
    STATUS_CHOICES = [
        ('onboarded', 'Onboarded'),
        ('offboarded', 'Offboarded'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  
    date_of_joining = models.DateField()
    date_of_exit = models.DateField(null=True, blank=True)
    department = models.ForeignKey('management.Department', on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='onboarded')

    def __str__(self):
        return self.name

