import django_filters
from .models import *
class MealsFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='iexact')
    maxcalories=django_filters.filters.NumberFilter(field_name='calories',lookup_expr='gte')
    mincalories=django_filters.filters.NumberFilter(field_name='calories',lookup_expr='lte')
    keyword=django_filters.filters.CharFilter(field_name='name',lookup_expr='icontains')
    maxprice=django_filters.filters.NumberFilter(field_name='price',lookup_expr='gte')
    minprice=django_filters.filters.NumberFilter(field_name='price',lookup_expr='lte')
    class Meta:
        model = Meal
        fields = ('keyword','mincalories','maxcalories','name','maxprice','minprice')





class OrderFilter(django_filters.FilterSet):

    customername = django_filters.CharFilter(lookup_expr='icontains',field_name='customer__first_name')
    #  status = django_filters.CharFilter(lookup_expr='icontains',field_name='customer__first_name')
    class Meta:
        model = Order
        fields=('customername','status')
