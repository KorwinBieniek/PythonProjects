from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'

db = SQLAlchemy(app)


class book(db.Model):
    id = db.Column('book_id', db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    pages = db.Column(db.Integer)


def __init__(self, title, author, genre, pages):
    self.title = title
    self.author = author
    self.genre = genre
    self.pages = pages


db.create_all()

odyssey_book = book(id=1, title='Odyssey', author='Homer',
                       genre='Epic poetry', pages=541)

art_of_war_book = book(id=2, title='Art Of War', author='Sun Tzu',
                       genre='Non-fiction', pages=260)

dune_book = book(id=3, title='Dune', author='Frank Herbert',
                       genre='Science Fiction', pages=412)

hobbit_book = book(id=4, title='The Hobbit', author='J. R. R. Tolkien',
                       genre='High Fantasy', pages=310)

harry_potter_book = book(id=5, title='Harry Potter and the Philosopher\'s Stone', author='J. K. Rowling',
                       genre='Fantasy', pages=223)

moby_dick_book = book(id=6, title='Moby Dick', author='Herman Melville',
                       genre='Adventure Fiction', pages=378)

fellowship_of_the_ring_book = book(id=7, title='The Fellowship of the Ring', author='J. R. R. Tolkien',
                       genre='Fantasy', pages=423)

don_quixote_book = book(id=8, title='Don Quixote', author='Miguel de Cervantes',
                       genre='Novel', pages=1077)

alice_in_wonderland_book = book(id=9, title='Alice\'s Adventures in Wonderland', author='Lewis Carroll',
                       genre='Fantasy', pages=109)

hamlet_book = book(id=10, title='Hamlet', author='William Shakespeare',
                       genre='Shakespearean tragedy', pages=218)
# db.session.add(odyssey_book)
# db.session.add(art_of_war_book)
# db.session.add(hobbit_book)
# db.session.add(harry_potter_book)
# db.session.add(moby_dick_book)
# db.session.add(fellowship_of_the_ring_book)
# db.session.add(don_quixote_book)
# db.session.add(alice_in_wonderland_book)
# db.session.add(hamlet_book)
# db.session.commit()


@app.route('/')
def main_page():  # put application's code here
    return render_template("index.html")


@app.route('/show_books', methods=['GET', 'POST'])
def show_books():
    return render_template("show_books.html", book=book.query.all())


@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    return render_template("borrow_book.html")


@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    return render_template("return_book.html")


@app.route('/see_users', methods=['GET', 'POST'])
def see_users():
    return render_template("see_users.html")


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    return render_template("add_user.html")


if __name__ == '__main__':
    app.run(debug=True)
