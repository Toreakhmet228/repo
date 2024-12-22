
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from .models import News, Category, Comment, Like
from .serializers import NewsSerializer, CategorySerializer, CommentSerializer

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

class AddCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        news_id = self.request.data.get('news')
        news = News.objects.get(id=news_id)
        user_id = self.request.data.get('user')
        user = User.objects.get(id=user_id)
        serializer.save(user=user, news=news)

class LikeNewsView(APIView):
    def post(self, request, news_id):
        news = News.objects.filter(id=news_id).first()
        if not news:
            return Response({"error": "News not found"}, status=404)

        user_id = request.data.get('user')
        user = User.objects.get(id=user_id)

        like, created = Like.objects.get_or_create(user=user, news=news)
        if not created:
            like.delete()
            return Response({"message": "Like removed"})
        return Response({"message": "News liked"})
