from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt
)
from app import db
from app.models import User, RefreshToken, TokenBlocklist, PasswordResetToken
from datetime import datetime, timezone
from uuid import uuid4
import secrets
from app.utils import send_password_reset_email
from app.routes.config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 409
    
    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    # Check if user exists
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Account is deactivated'}), 403
    
    # Generate tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Store refresh token in database
    expires_at = datetime.now(timezone.utc) + Config.JWT_REFRESH_TOKEN_EXPIRES
    new_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=expires_at
    )
    
    db.session.add(new_token)
    db.session.commit()
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200


@auth_bp.route('/api/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user_id = get_jwt_identity()
    jwt_id = get_jwt()['jti']
    
    # Create new tokens
    access_token = create_access_token(identity=current_user_id)
    refresh_token = create_refresh_token(identity=current_user_id)
    
    # Store new refresh token
    expires_at = datetime.now(timezone.utc) + Config.JWT_REFRESH_TOKEN_EXPIRES
    new_token = RefreshToken(
        user_id=current_user_id,
        token=refresh_token,
        expires_at=expires_at
    )
    
    # Revoke old refresh token
    revoked_token = TokenBlocklist(
        jti=jwt_id,
        type='refresh',
        user_id=current_user_id
    )
    
    db.session.add(new_token)
    db.session.add(revoked_token)
    db.session.commit()
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@auth_bp.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    jwt_id = get_jwt()['jti']
    user_id = get_jwt_identity()
    
    # Add token to blocklist
    revoked_token = TokenBlocklist(
        jti=jwt_id,
        type='access',
        user_id=user_id
    )
    
    db.session.add(revoked_token)
    db.session.commit()
    
    return jsonify({'message': 'Successfully logged out'}), 200


@auth_bp.route('/api/logout-all', methods=['POST'])
@jwt_required()
def logout_all():
    user_id = get_jwt_identity()
    
    # Revoke all refresh tokens for user
    RefreshToken.query.filter_by(user_id=user_id).delete()
    
    # Revoke current access token
    jwt_id = get_jwt()['jti']
    revoked_token = TokenBlocklist(
        jti=jwt_id,
        type='access',
        user_id=user_id
    )
    
    db.session.add(revoked_token)
    db.session.commit()
    
    return jsonify({'message': 'Successfully logged out from all devices'}), 200


@auth_bp.route('/api/password-reset-request', methods=['POST'])
def password_reset_request():
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'message': 'Email is required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        # Don't reveal that email doesn't exist
        return jsonify({'message': 'Password reset email sent if account exists'}), 200
    
    # Generate reset token
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + Config.PASSWORD_RESET_EXPIRES
    
    # Store token in database
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )
    
    db.session.add(reset_token)
    db.session.commit()
    
    # Send email with reset link
    send_password_reset_email(user.email, token)
    
    return jsonify({'message': 'Password reset email sent if account exists'}), 200


@auth_bp.route('/password-reset', methods=['POST'])
def password_reset():
    data = request.get_json()
    
    if not data or not data.get('token') or not data.get('password'):
        return jsonify({'message': 'Token and new password are required'}), 400
    
    # Find token in database
    reset_record = PasswordResetToken.query.filter_by(
        token=data['token'],
        is_used=False
    ).first()
    
    if not reset_record or reset_record.expires_at < datetime.now(timezone.utc):
        return jsonify({'message': 'Invalid or expired token'}), 400
    
    # Update user's password
    user = User.query.get(reset_record.user_id)
    user.set_password(data['password'])
    
    # Mark token as used
    reset_record.is_used = True
    
    # Revoke all refresh tokens for this user
    RefreshToken.query.filter_by(user_id=user.id).delete()
    
    db.session.commit()
    
    return jsonify({'message': 'Password has been reset successfully'}), 200