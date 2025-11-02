from bookshelf.models import Book

# Retrieve all books
books = Book.objects.all()

# Display details of each book
for b in books:
    print(b.id, b.title, b.author, b.publication_year)

# Expected Output:
# 1 1984 George Orwell 1949
