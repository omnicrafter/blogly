from flask import Flask, request, render_template, redirect, flash, session
from models import db, User, Post, Tag, PostTag
# from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "secretkey123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

app.app_context().push()


def connect_db(app):
    db.app = app
    db.init_app(app)


connect_db(app)


@app.route('/')
def home_page():
    """Shows home page"""

    return redirect('/users')


@app.route('/users')
def users_page():
    """Show all users"""

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def user_add_form():
    """Show User Add Form"""

    return render_template('add-user.html')


@app.route('/users/new', methods=["POST"])
def add_user():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"] or None

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show user details"""

    user = User.query.get_or_404(user_id)
    return render_template("user-details.html", user=user)


@app.route('/add-user')
def create_user_page():
    """Shows Create User Page"""

    return render_template('create-user.html')


@app.route('/user-detail')
def user_detail_page():
    """Shows User Details Page"""

    return render_template('user-details.html')


@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):
    """Shows Edit User Page"""

    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def user_update(user_id):
    """Update User"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"] or None

    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete User"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# Posts Routes (Part 2)


if __name__ == "__main__":
    app.run(debug=True)


@app.route('/users/<int:user_id>/posts/new')
def show_add_post_form(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('add-post.html', user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_add_post(user_id):
    """Handle add form: add post and redirect to the user detail page."""

    selected_tags = request.form.getlist("tags[]")
    user_id = user_id
    title = request.form["title"]
    content = request.form["content"]

    if not selected_tags:
        new_post = Post(title=title, content=content, user_id=user_id)

        db.session.add(new_post)
        db.session.commit()

    else:
        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        for tag in selected_tags:
            selected_tag = Tag.query.get(tag)
            new_post.tags.append(selected_tag)
        db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post."""

    post = Post.query.get_or_404(post_id)
    tags = post.tags

    return render_template('post-details.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    all_tags = Tag.query.all()
    post_tags = [tag.id for tag in post.tags]

    return render_template('edit-post.html', post=post, post_tags=post_tags, all_tags=all_tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    selected_tags = request.form.getlist("tags[]")
    post = Post.query.get_or_404(post_id)
    title = request.form["title"]
    content = request.form["content"]

    # Update Title and Content
    post.title = title
    post.content = content

    post.tags = [
        selected_tag for selected_tag in post.tags if selected_tag.id in selected_tags]

    # Add new tags
    for tag in selected_tags:
        selected_tag = Tag.query.get(tag)
        if selected_tag:
            post.tags.append(selected_tag)

    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete a post."""

    post = Post.query.get_or_404(post_id)
    user = post.user_info.id

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user}')

# Tags Routes (Part 3)


@app.route('/tags')
def show_tags():
    """Show all tags."""

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Show Tag Details."""

    tag = Tag.query.get_or_404(tag_id)
    tagged_posts = tag.posts

    return render_template('tag-details.html', tag=tag, tagged_posts=tagged_posts)


@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_page(tag_id):
    """Show edit tag page."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit-tag.html', tag=tag)


@app.route('/tags/new')
def show_add_tag_form():
    """Show form to add a tag."""

    return render_template('add-tag.html')


@app.route('/tags/new', methods=["POST"])
def handle_add_tag():
    """Handle add form: add tag and redirect to tag list."""

    name = request.form["name"]

    new_tag = Tag(name=name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def handle_edit_tag(tag_id):
    """Handle editing of a tag. Redirect back to the tag list."""

    tag = Tag.query.get_or_404(tag_id)
    name = request.form["name"]

    tag.name = name

    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')
