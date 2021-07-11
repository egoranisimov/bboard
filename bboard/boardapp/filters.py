from django_filters import FilterSet, DateFilter
from django.forms import DateInput
from .models import Advert, AdvertReply


class AdvertsFilter(FilterSet):
    datetime = DateFilter(field_name='datetime',
                          widget=DateInput(attrs={'type': 'date'}),
                          lookup_expr='gt',
                          label='Позже выбранной даты')

    class Meta:
        model = Advert
        fields = {
            'title': ['icontains'],
            'content': ['icontains'],
            'category': ['exact'],
            'author': ['exact']
        }


class RepliesFilter(FilterSet):

    datetime = DateFilter(field_name='datetime',
                          widget=DateInput(attrs={'type': 'date'}),
                          lookup_expr='gt',
                          label='Позже выбранной даты')

    class Meta:
        model = AdvertReply
        fields = {
            'advert': ['exact'],
            'author': ['exact']
        }
