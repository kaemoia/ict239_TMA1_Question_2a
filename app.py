from flask import Flask, render_template, request
from books import all_books 

# Initialize Flask application
app = Flask(__name__)  

def get_description_preview(description_list):
    """Get first and last paragraphs of description for preview"""
    if not description_list:
        return ""  # Return empty string if no description
    if len(description_list) == 1:
        return description_list[0]  # Return single paragraph as-is
    return description_list[0] + "..." + description_list[-1]  # Combine first and last paragraphs

def get_sorted_books():
    """Return books sorted by title in alphabetical order"""
    return sorted(all_books, key=lambda book: book['title'])

def filter_books_by_category(category):
    """Filter books by category (case-insensitive)"""
    if not category or category.lower() == 'all':
        return get_sorted_books()  # Return all books if no category specified
    
    filtered = []
    for book in all_books:
        if book['category'].lower() == category.lower():
            filtered.append(book)
    return sorted(filtered, key=lambda book: book['title'])  # Return filtered books sorted by title

@app.route('/')
@app.route('/books')
def books():
    """Main books listing page - MVC Controller"""
    category = request.args.get('category', '')  # Get category from URL parameters
    
    if category:
        book_list = filter_books_by_category(category)  # Filter books by category
    else:
        book_list = get_sorted_books()  # Get all sorted books
    
    # Add preview descriptions for display in View
    for book in book_list:
        book['preview_description'] = get_description_preview(book['description'])
    
    categories = ['Children', 'Teens', 'Adult']  # Available categories for filter dropdown
    
    return render_template('books.html',
                         books=book_list,
                         categories=categories,
                         selected_category=category)
                         
@app.route('/book/<string:book_title>')
def book_details(book_title):
    """Book details page - using book title as URL identifier"""
    # Find the book by title
    book = None
    book_index = -1
    
    for i, b in enumerate(all_books):
        if b['title'].lower() == book_title.lower():
            book = b
            book_index = i
            break
    
    if book is None:
        return "Book not found", 404  # Return 404 error if book does not exist
    
    return render_template('book_details.html', 
                         book=book, 
                         book_index=book_index,
                         all_books=all_books)