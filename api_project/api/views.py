from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewset(viewsets.ModelViewset):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    