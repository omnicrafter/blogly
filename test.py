from unittest import TestCase
from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

app.app_context().push()
db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for Model for Users."""

    def setUp(self):
        """Clean existing Users."""
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        db.session.remove()

    def test_default_image(self):
        """Test default image."""
        user = User(first_name="John", last_name="Doe")
        self.assertEqual(user.image_url, None)

    def test_add_user(self):
        """Test adding user."""
        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)

    def test_delete_user(self):
        """Test deleting user."""
        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 0)

    def test_update_user(self):
        """Test updating user."""
        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()
        user.first_name = "Jane"
        db.session.commit()
        self.assertEqual(user.first_name, "Jane")

    def test_user_details(self):
        """Test user details."""
        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.full_name, "John Doe")

    def test_user_list(self):
        """Test user list."""
        user1 = User(first_name="John", last_name="Doe")
        user2 = User(first_name="Jane", last_name="Doe")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 2)


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
        db.session.remove()

    def test_user_list(self):
        """Test user list."""

        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)

    def test_user_details(self):
        """Test user details."""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)

    def test_add_user(self):
        """Test adding user."""

        with app.test_client() as client:
            d = {"first-name": "Jane", "last-name": "Doe", "image-url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Jane Doe', html)

    def test_delete_user(self):
        """Test deleting user."""

        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('John Doe', html)


class PostModelTestCase(TestCase):
    """Tests for Model for Posts."""

    def setUp(self):
        """Clean existing Posts."""
        Post.query.delete()
        user1 = User(first_name="John", last_name="Doe")
        db.session.add(user1)
        db.session.commit()

        # Store the user ID for use in the tests
        self.user_id = user1.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        Post.query.delete()
        User.query.delete()
        db.session.commit()

        db.session.rollback()
        db.session.remove()

    def test_add_post(self):
        """Test adding post."""
        post = Post(title="First Post",
                    content="This is my first post", user_id=1)
        db.session.add(post)
        db.session.commit()
        self.assertEqual(len(Post.query.all()), 1)

    def test_delete_post(self):
        """Test deleting post."""
        post = Post(title="First Post",
                    content="This is my first post", user_id=1)
        db.session.add(post)
        db.session.commit()
        db.session.delete(post)
        db.session.commit()
        self.assertEqual(len(Post.query.all()), 0)

    def test_update_post(self):
        """Test updating post."""
        post = Post(title="First Post",
                    content="This is my first post", user_id=1)
        db.session.add(post)
        db.session.commit()
        post.title = "Second Post"
        db.session.commit()

        # Fetch the updated post from the database
        updated_post = Post.query.filter_by(user_id=1).first()

        self.assertEqual(updated_post.title, "Second Post")


class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

        # Add a test user for the routes that require a user
        user = User(first_name="John", last_name="Doe")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

        # Add a test post for the post-related routes
        post = Post(title="Test Post", content="Test Content",
                    user_id=self.user_id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id

    def tearDown(self):
        db.session.rollback()
        db.session.remove()

    def test_show_add_post_form(self):
        response = self.client.get(f'/users/{self.user_id}/posts/new')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add Post for', response.data)

    def test_handle_add_post(self):
        data = {
            'title': 'New Post Title',
            'content': 'New Post Content'
        }
        response = self.client.post(
            f'/users/{self.user_id}/posts/new', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New Post Title', response.data)

    def test_show_post(self):
        response = self.client.get(f'/posts/{self.post_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Post', response.data)

    def test_show_edit_post_form(self):
        response = self.client.get(f'/posts/{self.post_id}/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Post', response.data)

    def test_handle_edit_post(self):
        data = {
            'title': 'Updated Post Title',
            'content': 'Updated Post Content'
        }
        response = self.client.post(
            f'/posts/{self.post_id}/edit', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Post Title', response.data)

    def test_delete_post(self):
        response = self.client.post(
            f'/posts/{self.post_id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Test Post', response.data)
