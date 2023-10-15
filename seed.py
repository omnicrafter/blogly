
from models import User, Post, Tag, PostTag, db
from app import app

with app.app_context():
    # Create all tables
    db.drop_all()
    db.create_all()

# If table isn't empty, empty it
    User.query.delete()

# Add users
    user1 = User(first_name="John", last_name="Doe",
                 image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
    user2 = User(first_name="Jane", last_name="Doe",
                 image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
    user3 = User(first_name="Bob", last_name="Doe",
                 image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
    user4 = User(first_name="Sally", last_name="Doe",
                 image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")

# Add new objects to session, so they'll persist
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)

# Add posts
    post1 = Post(title="First Post",
                 content="This is my first post", user_id=1)
    post2 = Post(title="Second Post",
                 content="This is my second post", user_id=2)
    post3 = Post(title="Third Post",
                 content="This is my third post", user_id=3)
    post4 = Post(title="Fourth Post",
                 content="This is my fourth post", user_id=4)
    post5 = Post(title="Fifth Post",
                 content="This is my fifth post", user_id=1)
    post6 = Post(title="Sixth Post",
                 content="This is my sixth post", user_id=2)
    post7 = Post(title="Seventh Post",
                 content="This is my seventh post", user_id=3)
    post8 = Post(title="Eighth Post",
                 content="This is my eighth post", user_id=4)

    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.add(post4)
    db.session.add(post5)
    db.session.add(post6)
    db.session.add(post7)
    db.session.add(post8)

# Add Tags
    tag1 = Tag(name="Fun")
    tag2 = Tag(name="Happy")
    tag3 = Tag(name="Sad")
    tag4 = Tag(name="Excited")
    tag5 = Tag(name="Bored")
    tag6 = Tag(name="Tired")
    tag7 = Tag(name="Angry")
    tag8 = Tag(name="Hungry")

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.add(tag4)
    db.session.add(tag5)
    db.session.add(tag6)
    db.session.add(tag7)
    db.session.add(tag8)

# Commit--otherwise, this never gets saved!
    db.session.commit()
