from django.forms import DateInput
from django_filters import FilterSet, DateFilter, DateFromToRangeFilter, CharFilter, ModelChoiceFilter
from django_filters.widgets import RangeWidget

from .models import Post, Author


class PostFilter(FilterSet):
    name = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Поиск по названию'
    )

    author = ModelChoiceFilter(
        queryset=Author.objects.all(),
        label='Автор',
        empty_label="Все авторы",
    )

    date = DateFilter(
        field_name='time_in',
        lookup_expr='date',
        widget=DateInput(attrs={'type': 'date'}),
        label='Точная дата')

    date_between = DateFromToRangeFilter(
        field_name='time_in',
        lookup_expr='date',
        widget=RangeWidget(attrs={'type': 'date'}),
        label='Диапозон дат'
    )

    class Meta:
        model = Post
        fields = {}
