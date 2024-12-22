from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .models import News, Category
from .serializers import NewsSerializer, CategorySerializer

class NewsListView(ListAPIView):
    queryset = News.objects.all().order_by('-date_added')
    serializer_class = NewsSerializer

class NewsByCategoryView(APIView):
    def get(self, request, category_name):
        category = Category.objects.filter(name__iexact=category_name).first()
        if not category:
            return Response({"error": "Category not found"}, status=404)
        news = News.objects.filter(category=category).order_by('-date_added')
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)
