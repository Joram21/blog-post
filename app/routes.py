from flask import Blueprint, jsonify, request
from .models import db, User, Post, Comment
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@main.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([post.to_dict() for post in posts]), 200

@main.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    user_id = get_jwt_identity()
    new_post = Post(title=data['title'], content=data['content'], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return jsonify(new_post.to_dict()), 201

# More routes for updating, deleting posts, and handling comments...
