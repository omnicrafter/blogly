from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """User"""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                           nullable=False)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMAGE_URL)

    # user_posts = db.relationship('Post') <-- using backref on Posts model

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name}>"

    @property
    def full_name(self):
        """Return full name of the user"""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post Model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False, default="No Content")
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user_info = db.relationship('User', backref='posts')

    tags = db.relationship('Tag', secondary='post_tags',
                           backref='posts')

    def __repr__(self):
        return f"<Post {self.id} {self.title} {self.content} {self.created_at} {self.user_id}>"


class Tag(db.Model):
    """Tag Model"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"


class PostTag(db.Model):
    """PostTag Model"""

    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        return f"<PostTag {self.post_id} {self.tag_id}>"
