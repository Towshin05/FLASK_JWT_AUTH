from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, RefreshToken, TokenBlocklist

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/me', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat()
    }), 200


@user_bp.route('/api/me', methods=['PUT'])
@jwt_required()
def update_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    # Update username if provided
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 409
        user.username = data['username']
    
    # Update email if provided
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 409
        user.email = data['email']
    
    # Update password if provided
    if 'password' in data and data.get('current_password'):
        if not user.check_password(data['current_password']):
            return jsonify({'message': 'Current password is incorrect'}), 401
        user.set_password(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active
        }
    }), 200


@user_bp.route('/api/me', methods=['DELETE'])
@jwt_required()
def deactivate_account():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Revoke all refresh tokens
    RefreshToken.query.filter_by(user_id=user.id).delete()
    
    # Deactivate user account
    user.is_active = False
    db.session.commit()
    
    return jsonify({'message': 'Account deactivated successfully'}), 200


@user_bp.route('/api/sessions', methods=['GET'])
@jwt_required()
def get_active_sessions():
    current_user_id = get_jwt_identity()
    
    # Get all active refresh tokens for the user
    active_tokens = RefreshToken.query.filter_by(user_id=current_user_id).all()
    
    sessions = [{
        'id': token.id,
        'created_at': token.created_at.isoformat(),
        'expires_at': token.expires_at.isoformat()
    } for token in active_tokens]
    
    return jsonify({'active_sessions': sessions}), 200


@user_bp.route('/api/sessions/<session_id>', methods=['DELETE'])
@jwt_required()
def revoke_session(session_id):
    current_user_id = get_jwt_identity()
    
    # Find the session
    token = RefreshToken.query.filter_by(
        id=session_id,
        user_id=current_user_id
    ).first()
    
    if not token:
        return jsonify({'message': 'Session not found'}), 404
    
    # Delete the refresh token
    db.session.delete(token)
    db.session.commit()
    
    return jsonify({'message': 'Session revoked successfully'}), 200