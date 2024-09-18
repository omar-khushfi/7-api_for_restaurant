from django.db import models
from django.contrib.auth.models import User

from django.db import models


class OrderStatus(models.TextChoices):
    COOkING='cooking'
    INQUEUE='in_queue'
    EATING='eating'


class Meal(models.Model):
    name = models.CharField(max_length=255)  
    price = models.DecimalField(max_digits=6, decimal_places=2)  
    image = models.ImageField(upload_to='meal_images/',default='meal_images/no_photo.png')  
    description = models.TextField()  
    is_available = models.BooleanField(default=True)  
    calories=models.IntegerField(default=0)
    rating=models.DecimalField(default=0,max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name



class Food(models.Model):
    name = models.CharField(max_length=255) 
    def __str__(self):
        return self.name



class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE) 
    meals = models.ManyToManyField(Meal)  
    order_date = models.DateTimeField(auto_now_add=True) 
    status=models.CharField(max_length=30,choices=OrderStatus,default=OrderStatus.INQUEUE)
    total=models.DecimalField(max_digits=6,decimal_places=2,default=0)
    
    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"

    def save(self, *args, **kwargs):
        self.total = sum(meal.price for meal in self.meals.all())
        super().save(*args, **kwargs)




class Review(models.Model):
    meal=models.ForeignKey(Meal,on_delete=models.CASCADE,related_name="reviews")
    customer=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    rating=models.DecimalField(default=0,max_digits=3, decimal_places=2)
    comment=models.TextField(max_length=1000,default="",blank=False)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment
    