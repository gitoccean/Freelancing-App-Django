from django.db import models


# Create your models here.


class Jobs(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed")
    ])
    date = models.DateField()

    def __str__(self):
        return self.title


from django.contrib.auth.models import User


class extended(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    img = models.ImageField()

    def __str__(self):
        return str(self.id)
