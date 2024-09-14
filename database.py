from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    added = db.Column(db.DateTime, nullable=False, default=func.now())
    author = db.Column(db.String)
    is_read = db.Column(db.Boolean)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id", ondelete="SET NULL"))
    genre = relationship("Genre", back_populates="books")

    def __repr__(self):
        return f"Book(title={self.fullname!r}"


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    books = relationship("Book", back_populates="genre")

    def __repr__(self):
        return f"Genre(name={self.name!r}"
