from .models import Todo
from rest_framework import serializers


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ('user', 'text', 'is_completed', 'created_time', 'last_updated')

