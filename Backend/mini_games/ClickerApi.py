from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from flask_sqlalchemy import SQLAlchemy

# Create blueprint
clicker_api = Blueprint('clicker_api', __name__)

# Create a function to initialize the database
def init_db(db_instance, User_model):
    global db, User
    db = db_instance
    User = User_model

@clicker_api.route('/api/clicker/leaderboard', methods=['GET'])
@jwt_required()
def get_clicker_leaderboard():
    top_users = (
        db.session.query(User)
        .filter(User.username != None, User.username != '')
        .order_by(User.fitte_points.desc())
        .limit(20)
       .all()
    )
    return jsonify([
        {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'fitte_points': user.fitte_points
        }
        for user in top_users
    ]), 200