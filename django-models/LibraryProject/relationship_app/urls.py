from django.urls import path
from . import views
from .views import list_books
from .views import LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path("admin-role/", views.admin_view, name="admin_view"),
    path("librarian-role/", views.librarian_view, name="librarian_view"),
    path("member-role/", views.member_view, name="member_view"),
    path(
        'login/',
        LoginView.as_view(template_name='relationship_app/templates/relationship_app/login.html'),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(template_name='relationship_app/templates/relationship_app/logout.html'),
        name='logout'
    ),

    # Registration (custom view)
    path('register/', views.register_view, name='register'),

    path('books/', list_books, name='list_books'),  # Function-based view
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),  # Class-based view
]



