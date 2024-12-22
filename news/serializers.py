from rest_framework import serializers
from .models import News, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'category', 'image', 'date_added']
