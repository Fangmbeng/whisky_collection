from flask import Blueprint, request, jsonify
from app.models import db, Post, User
from forms import PostForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user


api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Get data from form
        brand = form.brand.data
        alcohol_level = form.alcohol_level.data
        class_alcohol = form.class_alcohol.data
        # Create new post instance which will also add to db
        new_post = Post(brand=brand, alcohol_level=alcohol_level, class_alcohol=class_alcohol, user_id=current_user.id)
        flash(f"{new_post.brand} has been created", "success")
        return redirect(url_for('site.index'))
        
    return render_template('create.html', form=form)

@api.route('/posts/<int:post_id>')
@login_required
def get_post(post_id):
    # post = Post.query.get_or_404(post_id)
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('site.index'))
    return render_template('post.html', post=post)


@api.route('/posts/<post_id>/edit', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('site.index'))
    # Make sure the post author is the current user
    if post.author != current_user:
        flash("You do not have permission to edit this post", "danger")
        return redirect(url_for('site.index'))
    form = PostForm()
    if form.validate_on_submit():
        # Get the form data
        brand = form.brand.data
        alcohol_level = form.alcohol_level.data
        class_alcohol = form.class_level
        
        # update the post using the .update method
        post.update(brand=brand, alcohol_level=alcohol_level, class_alcohol=class_alcohol)
        flash(f"{post.brand} has been updated!", "success")
        return redirect(url_for('api.get_post', post_id=post.id))
    if request.method == 'GET':
        form.brand.data = post.brand
        form.alcohol_level.data = post.alcohol_level
        form.class_alcohol = post.class_alcohol
    return render_template('edit_post.html', post=post, form=form)

# DELETE car ENDPOINT

@api.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash(f"A post with id {post_id} does not exist", "danger")
        return redirect(url_for('site.index'))
    # Make sure the post author is the current user
    if post.author != current_user:
        flash("You do not have permission to delete this post", "danger")
        return redirect(url_for('site.index'))
    post.delete()
    flash(f"{post.brand} has been deleted", "info")
    return redirect(url_for('site.index'))

#routes for JSON request
#from app.blueprints.authentication.auth import basic_auth, token_auth


@api.route('/token')
#@basic_auth.login_required
def index_():
    user = User.username
    token = user.get_token()
    return {'token':token, 'token_expiration':user.token_expiration}

@api.route('/post', methods=['GET'])
def getposts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])
        

@api.route('/post/<int:post_id>')
def getpost(post_id):
    posts = Post.query.get(post_id)
    return posts.to_dict()

@api.route('/posts', methods=['POST'])
#@token_auth.login_required
def createpost():
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['brand', 'alcohol_level', 'class_alcohol']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    brand = data.get('brand')
    alcohol_level = data.get("alcohol_level")
    class_alcohol = data.get("class_alcohol")
    #user = data.get('')
    new_post = Post(brand=brand, alcohol_level=alcohol_level, class_alcohol=class_alcohol) #user_id=user.id
    return new_post.to_dict(), 201
    

@api.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    return user.to_dict()

@api.route('/user', methods=['GET','POST'])
def get_username():
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['username', 'password']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    #email = data.get('email')
    username = data.get("username")
    password = data.get('password')
            # Query our user table to see if there are any users with either username or email from form
    get_user = User.query.filter_by(username=username).first()
        # If the query comes back with any results
    if get_user is None:
        return ('Please Sign Up to create an account.'), 400
    elif get_user is not None and get_user.check_password(password):
        # log the user in
        login_user(get_user)
    return get_user.to_dict(), 201


@api.route('/users', methods=['POST'])
def createuser():
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['email', 'username', 'password']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    email = data.get('email')
    username = data.get("username")
    password = data.get('password')
            # Query our user table to see if there are any users with either username or email from form
    check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        # If the query comes back with any results
    if check_user:
        return ('A user with that email and/or username already exists.'), 400
    new_user = User(email=email, password=password, username= username)
    return new_user.to_dict(), 201
    
@api.route('/post/edit/<int:post_id>', methods=['POST'])
#@token_auth.login_required
def editpost(post_id):
    post = Post.query.get(post_id)
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['brand', 'alcohol_level', 'class_alcohol']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    brand = data.get('brand')
    alcohol_level = data.get("alcohol_level")
    class_alcohol = data.get("class_alcohol")
    #user = token_auth.current_user()
    post.update(brand=brand, alcohol_level=alcohol_level, class_alcohol= class_alcohol) #user_id=user)
    return post.to_dict(), 201


@api.route('/post/delete/<int:post_id>', methods=['POST'])
#@token_auth.login_required
def deletepost(post_id):
    post = Post.query.get(post_id)
    if not request.is_json:
        return("your request content-type is not JSON"), 400
    data=request.json
    for field in ['brand', 'alcohol_level', 'class_alcohol']:
        if field not in data:
            return("error:f{field} must be in request body"), 400
    post.delete()
    return post.to_dict(), 201