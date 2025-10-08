from flask import Flask, render_template, request
from books import all_books

app = Flask(__name__)

def get_description_preview(description_list):
    """Get first and last paragraphs of description"""
    if not description_list:
        return ""
    if len(description_list) == 1:
        return description_list[0]
    return description_list[0] + "..." + description_list[-1]

def get_sorted_books():
    """Return books sorted by title"""
    return sorted(all_books, key=lambda book: book['title'])

def filter_books_by_category(category):
    """Filter books by category"""
    if not category or category.lower() == 'all':
        return get_sorted_books()
    
    filtered = []
    for book in all_books:
        if book['category'].lower() == category.lower():
            filtered.append(book)
    return sorted(filtered, key=lambda book: book['title'])

@app.route('/')
@app.route('/books')
def books():
    """Main books listing page - MVC Controller"""
    category = request.args.get('category', '')
    
    if category:
        book_list = filter_books_by_category(category)
    else:
        book_list = get_sorted_books()
    
    # Add preview descriptions for View
    for book in book_list:
        book['preview_description'] = get_description_preview(book['description'])
    
    categories = ['Children', 'Teens', 'Adult']
    
    return render_template('books.html',
                         books=book_list,
                         categories=categories,
                         selected_category=category)
                         
@app.route('/book/<string:book_title>')
def book_details(book_title):
    """Book details page - using book title as identifier"""
    # Find the book by title
    book = None
    book_index = -1
    
    for i, b in enumerate(all_books):
        if b['title'].lower() == book_title.lower():
            book = b
            book_index = i
            break
    
    if book is None:
        return "Book not found", 404
    
    return render_template('book_details.html', 
                         book=book, 
                         book_index=book_index,
                         all_books=all_books)