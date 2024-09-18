from audioop import avg
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from .models import *
from .serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .filters import *
from django.db.models import Avg
# Create your views here.


#####accounts######

@api_view(['POST'])
def register(request):
    data=request.data
    user=SignUpserializer(data=data)
    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['username'],
                password=make_password(data['password'])
            )
            return Response({'details':' your account registered '},status=status.HTTP_201_CREATED)
        else:
            return Response({'details':' this email already exists '},status=status.HTTP_400_BAD_REQUEST)
    else :
        return Response({'details':user.errors},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user=SignUpserializer(request.user)
    return Response(user.data)


####################


###########food############
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_food(request):
    data=request.data
    serializer=foodserializer(data=data)
    if serializer.is_valid():
        if not Food.objects.filter(name=data['name']).exists():
            Food.objects.create(
            name=data['name']
             )
            return Response({"details":"the food is add"},status=status.HTTP_201_CREATED)
        else:
            return Response({'details':' this food already exists '},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_food(request,pk):
    food=get_object_or_404(Food,pk=pk)
    food.delete()
    return Response({"details":"Delelte is done "})
    
    
####################



########meal###########
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_meal(request):
    serializer = MealSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def meal(request,pk):
    food=get_object_or_404(Meal,pk=pk)
    serializer=MealSerializer(food,many=False)
    return Response(serializer.data)


@api_view(['GET'])
def meals(request):
    meals=Meal.objects.all().order_by('id')
    filterset=MealsFilter(request.GET,queryset=meals)
    respage=4
    countpage=filterset.qs.count()
    paginator=PageNumberPagination()
    paginator.page_size=respage
    queryset=paginator.paginate_queryset(filterset.qs,request)
    serializer=MealSerializer(queryset,many=True)
    return Response({"meals":serializer.data,"count":countpage})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_meal(request,pk):
    data=request.data
    meal=get_object_or_404(Meal,pk=pk)
    meal.name=data['name']
    meal.price=data['price']
    meal.calories=data['calories']
    meal.is_available=data['is_available']
    meal.description=data['description']
    meal.image=data['image']
    meal.save()
    serializer=MealSerializer(meal,many=False)
    return Response(serializer.data)
    
##########################




#######order#######


@api_view(['GET'])
def orders(request):
    orders=Order.objects.all().order_by('order_date')
    filterset=OrderFilter(request.GET,queryset=orders)
    respage=4
    countpage=filterset.qs.count()
    paginator=PageNumberPagination()
    paginator.page_size=respage
    queryset=paginator.paginate_queryset(filterset.qs,request)
    serializer=OrderSerializer(queryset,many=True)
    return Response({"orders":serializer.data,"count":countpage})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order(request,pk):
    order=get_object_or_404(Order,pk=pk)
    serializer=OrderSerializer(order,many=False)
    return Response({"order":serializer.data})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order(request,pk):
    data=request.data
    order=get_object_or_404(Order,pk=pk)
    customer=User.objects.get(id=data['customer'])
    order.customer=customer
    order.meals.set(data['meals'])
    order.status=data['status']
    serializer=OrderSerializer(order,many=False)
    return Response({"order":serializer.data})
    

###################



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request,pk):
    data=request.data
    meal=get_object_or_404(Meal,pk=pk)
    user=request.user
    review=meal.reviews.filter(customer=user)
    
    if data['rating'] >5 or data['rating'] <0:
        return Response({"error":" the rate between 0 -> 5"},status=status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        new_review={'rating':data['rating'],'comment':data['comment']}
        review.update(**new_review)
        rating=meal.reviews.aggregate(avg_ratings=Avg('rating'))
        meal.rating=rating['avg_ratings']
        meal.save()
        return Response({"details":" meal review updated"})
    else:
        Review.objects.create(
            customer=user,
            meal=meal,
            rating=data['rating'],
            comment=data['comment']
        )
        rating=meal.reviews.aggregate(avg_ratings=Avg('rating'))
        meal.rating=rating['avg_ratings']
        meal.save()
        return Response({"details":" meal review created"})


        

@api_view(['DELETE'])
@permission_classes ([IsAuthenticated]) 
def delete_review(request, pk):
    user = request.user
    meal = get_object_or_404(Meal,id=pk)
    review = meal.reviews.filter(customer=user)
    if review.exists():
        review.delete() 
        rating=meal.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating ['avg_ratings'] = 0
            meal.ratings = rating['avg_ratings'] 
            meal.save()
            return Response({'details':'meal review deleted'})
    return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)





@api_view(['GET'])
def review(request,pk):
    meal=get_object_or_404(Meal,pk=pk)
    reviews=Review.objects.filter(meal__pk=pk)
    respage=4
    countpage=reviews.count()
    paginator=PageNumberPagination()
    paginator.page_size=respage
    queryset=paginator.paginate_queryset(reviews,request)
    serializer=ReviewSerializer(queryset,many=True)
    mealserializer=MealNameSerializer(meal,many=False)
    return Response({"the meal is :":mealserializer.data,"reviews":serializer.data,"count":countpage})
