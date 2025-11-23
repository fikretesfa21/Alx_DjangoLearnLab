from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, permission_required
from django import forms
from .models import Library, Book # Assuming Library and Book are still needed

# --- IMPORT FIX: Ensure your models are imported correctly based on your file structure ---
# NOTE: If your app is 'bookshelf', you must ensure 'bookshelf' is in INSTALLED_APPS.
# We will use 'bookshelf' in the permission strings.

# =========================================================================
# BOOK MANAGEMENT (CRUD) VIEWS
# =========================================================================

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_year']


# View protected by NEW custom 'can_create' permission
# App name changed from relationship_app to bookshelf
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()

    # NOTE: Assuming templates are under 'relationship_app' directory still
    return render(request, "relationship_app/add_book.html", {"form": form})


# View protected by NEW custom 'can_edit' permission
# App name changed from relationship_app to bookshelf
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)

    return render(request, "relationship_app/edit_book.html", {"form": form})


# View protected by NEW custom 'can_delete' permission
# App name changed from relationship_app to bookshelf
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    # You must check for POST here for proper deletion flow (as you included)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})


# Function-based view: List all books
# View protected by NEW custom 'can_view' permission
# App name changed from relationship_app to bookshelf
@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    # Use the full app-relative path to the template
    return render(request, 'relationship_app/list_books.html', {'books': books})


# =========================================================================
# ROLE-BASED VIEWS (KEEPING YOUR EXISTING ROLE CHECKS)
# =========================================================================

# ---- Role Check Functions ----
# Assuming UserProfile and roles are defined in models.py
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


# ---- Admin View ----
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


# ---- Librarian View ----
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


# ---- Member View ----
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# =========================================================================
# AUTHENTICATION VIEWS
# =========================================================================

# User Registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


# User Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')     # redirect to any page you want
    else:
        form = AuthenticationForm()

    return render(request, 'relationship_app/login.html', {'form': form})


# User Logout
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')


# Class-based view: Show details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'