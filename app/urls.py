from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
  path('signup/',views.register,name="register"),
  path('userinfo/',views.current_user,name="userinfo"),
  
  
  path('add-food/',views.add_food,name="addfood"),
   path('delete-food/<int:pk>/',views.delete_food,name="deletfood"),
   
   
   path('add-meal/',views.add_meal,name="addmeal"),
   path('meal/<int:pk>/',views.meal,name="meal"),
   path('meals/',views.meals,name="meals"),
   path('update-meal/<int:pk>/',views.update_meal,name="updatemeal"),
   
   
    path('order/<int:pk>/',views.order,name="order"),
     path('orders/',views.orders,name="orders"),
     path('add-order/',views.add_order,name="addorder"),
     path('update-order/<int:pk>/',views.update_order,name="updateorder"),
     
     
     
        path('add/review/<int:pk>/',views.add_review,name='review'),
         path('review/delete/<int:pk>/',views.delete_review,name='delete_review'),
                  path('reviews/<int:pk>/',views.review,name='reviews'),


   
]
