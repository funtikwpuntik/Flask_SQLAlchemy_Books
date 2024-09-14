from flask import Flask, render_template, request
from data import genres_data, books_data
from database import db, Genre, Book

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.add_all(genres_data)
    db.session.add_all(books_data)

    db.session.commit()


@app.route("/", methods=['GET', 'POST'])
def all_books():
    books = Book.query.all()
    books.reverse()
    if request.method == 'POST':
        read_books = request.form.getlist('is_read')
        result = f"Вы прочитали: {len(read_books)} книг(и)"
        for book_id in read_books:
            book = db.session.get(Book, int(book_id))
            book.is_read = True
            db.session.commit()
        return render_template('all_books.html', result=result, books=books[:15], read_books=[int(id) for id in read_books])

    return render_template("all_books.html", books=books[:15])


@app.route("/genre/<int:genre_id>")
def books_by_genre(genre_id):
    genre = Genre.query.get_or_404(genre_id)
    return render_template(
        "books_by_genre.html",
        genre_name=genre.name,
        books=genre.books
    )


if __name__ == '__main__':
    app.run()
