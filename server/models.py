from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))  # Ensure 10 digits
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        # Ensure all authors have a name
        if not value:
            raise ValueError("Author must have a name")
        return value

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, value):
        # Ensure all posts have a title
        if not value:
            raise ValueError("Post must have a title")
        return value

    @validates('content')
    def validate_content_length(self, key, value):
        # Ensure post content is at least 250 characters long
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return value

    @validates('summary')
    def validate_summary_length(self, key, value):
        # Ensure post summary is at most 250 characters long
        if len(value) > 250:
            raise ValueError("Post summary cannot exceed 250 characters")
        return value

    @validates('category')
    def validate_category(self, key, value):
        # Ensure post category is either 'Fiction' or 'Non-Fiction'
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Invalid post category")
        return value

    @validates('title')
    def validate_clickbait_title(self, key, value):
        # Ensure the title is sufficiently clickbait-y
        clickbait_phrases = ["Won't Believe", "Secret", "Top [0-9]+", "Guess"]
        pattern = '|'.join(clickbait_phrases)
        if not re.search(pattern, value):
            raise ValueError("Post title is not clickbait-y enough")
        return value
