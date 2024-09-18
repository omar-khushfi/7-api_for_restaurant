from rest_framework import serializers
from .models import *

class SignUpserializer(serializers.ModelSerializer):
   class Meta:
        model=User
        fields=('first_name','last_name','email','password')
        extra_kwargs={
        'first_name':{'required':True,'allow_blank':False},
        'last_name':{'required':True,'allow_blank':False},
        'email':{'required':True,'allow_blank':False},
        'password':{'required':True,'allow_blank':False,'min_length':8},
        }
        
        
        
class foodserializer(serializers.ModelSerializer):
        class Meta:
           model=Food
           fields="__all__"     
        
        

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__' 
        


class MealNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id','name'] 
        
        
class OrderSerializer(serializers.ModelSerializer):
    meals = MealNameSerializer(many=True)
    customer_first_name = serializers.CharField(source='customer.first_name', read_only=True) 
    customer_last_name = serializers.CharField(source='customer.last_name', read_only=True) 
    
    class Meta:
        model = Order
        fields = ['id', 'customer_first_name', 'customer_last_name', 'meals', 'order_date', 'status', 'total']
        
        
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__' 
        

