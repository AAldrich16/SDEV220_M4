from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publisher = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Book(id={self.id}, book_name='{self.book_name}', author='{self.author}', publisher='{self.publisher}')"

# Create a book
@app.route('/books', methods=['POST'])
def create_book():
    # Get Book info
    book_data = request.get_json()
    # Create new book
    new_book = Book(book_name=book_data['book_name'], author=book_data['author'], publisher=book_data['publisher'])
    # Add new book to database
    db.session.add(new_book)
    db.session.commit()
    # return book info
    return jsonify({'message': 'Book created', 'book': {'id': new_book.id, 'book_name': new_book.book_name, 'author': new_book.author, 'publisher': new_book.publisher}})

# Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    # Grab all books
    books = Book.query.all()
    # For each book in `books`
    book_list = []
    for book in books:
        # Make dict template for array
        book_dict = {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}
        # push template to array
        book_list.append(book_dict)
    #return JSON'd array of books
    return jsonify(book_list)

# Get a book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Grab book by ID
    book = Book.query.get_or_404(book_id)
    #return a JSON of the book
    return jsonify({'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    # Get update information
    book_data = request.get_json()
    # Get the book
    book = Book.query.get_or_404(book_id)
    # Update the book
    book.book_name = book_data['book_name']
    book.author = book_data['author']
    book.publisher = book_data['publisher']
    # Commit changes to the database
    db.session.commit()
    # return updated book
    return jsonify({'message': 'Book updated', 'book': {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}})

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # see if book exists
    book = Book.query.get_or_404(book_id)
    # delete book
    db.session.delete(book)
    db.session.commit()
    # return message
    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)
