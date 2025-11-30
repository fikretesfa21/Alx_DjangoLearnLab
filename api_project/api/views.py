from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer
# your_app/views.py

from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated, 
    IsAuthenticatedOrReadOnly, 
    IsAdminUser
)
# your_app/views.py

from .permissions import IsOwnerOrReadOnly # ⬅️ Import the custom class

class UserPostViewSet(viewsets.ModelViewSet):
    # ...
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # NOTE: IsAuthenticated ensures the user is logged in first.
    # IsOwnerOrReadOnly then checks the object-level ownership.
# from .models import Item
# from .serializers import ItemSerializer

# 📝 Example A: Requires Authentication for ALL actions
class ProtectedItemViewSet(viewsets.ModelViewSet):
    # queryset = Item.objects.all()
    # serializer_class = ItemSerializer
    
    # User MUST provide a valid token
    permission_classes = [IsAuthenticated] 

# 📝 Example B: Read access for all, Write access for authenticated users
class PublicFeedViewSet(viewsets.ModelViewSet):
    # queryset = Item.objects.all()
    # serializer_class = ItemSerializer
    
    # Anonymous users can GET, Authenticated users can POST, PUT, DELETE
    permission_classes = [IsAuthenticatedOrReadOnly]

# 📝 Example C: Restricted to Staff/Admin Users
class SettingsViewSet(viewsets.ModelViewSet):
    # queryset = Item.objects.all()
    # serializer_class = ItemSerializer
    
    # Only Django users with is_staff=True can access
    permission_classes = [IsAdminUser]
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

