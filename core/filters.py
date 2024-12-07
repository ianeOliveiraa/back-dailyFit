from django_filters import rest_framework as filters
from core import models




class UserProfileFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='unaccent__icontains')

    class Meta:
        model = models.UserProfile
        fields = ['name']


class MuscleGroupFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='unaccent__icontains')

    class Meta:
        model = models.MuscleGroup
        fields = ['name']


class ExerciseFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='unaccent__icontains')
    category = filters.CharFilter(lookup_expr='unaccent__icontains')
    muscle_group = filters.CharFilter(lookup_expr='unaccent__icontains')

    class Meta:
        model = models.Exercise
        fields = ['name', 'category', 'muscle_group']

