from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from .models import Library , Book
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# ---- Role Check Functions ----
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

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()
    # Use the full app-relative path to the template
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view: Show details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'













































