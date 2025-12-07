from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# ListView: Retrieve all books (accessible to everyone)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only publicly allowed


# DetailView: Retrieve a single book by ID (accessible to everyone)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Read-only publicly allowed


# CreateView: Add a new book (restricted to authenticated users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    # Ensure proper handling and validation
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


# UpdateView: Modify an existing book (restricted to authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Ensure proper validation before saving
    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


# DeleteView: Remove a book (restricted to authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
