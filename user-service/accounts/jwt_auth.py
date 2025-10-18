"""
JWT authentication utilities
"""
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

User = get_user_model()


def create_access_token(user):
    """Create JWT access token"""
    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'username': user.username,
        'exp': datetime.utcnow() + settings.JWT_ACCESS_TOKEN_LIFETIME,
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def create_refresh_token(user):
    """Create JWT refresh token"""
    payload = {
        'user_id': str(user.id),
        'exp': datetime.utcnow() + settings.JWT_REFRESH_TOKEN_LIFETIME,
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def create_tokens(user):
    """Create both access and refresh tokens"""
    return {
        'access_token': create_access_token(user),
        'refresh_token': create_refresh_token(user),
        'token_type': 'bearer',
        'expires_in': int(settings.JWT_ACCESS_TOKEN_LIFETIME.total_seconds())
    }


def verify_token(token):
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')


def get_user_from_token(token):
    """Get user from JWT token"""
    payload = verify_token(token)
    user_id = payload.get('user_id')
    
    if not user_id:
        raise Exception('Invalid token payload')
    
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        raise Exception('User not found')


class JWTAuthentication(authentication.BaseAuthentication):
    """
    JWT authentication class for Django REST Framework
    Extracts JWT token from Authorization header and authenticates user
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return (user, auth) tuple
        Returns None if authentication is not attempted
        """
        import logging
        logger = logging.getLogger(__name__)
        
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        logger.info(f"JWT Auth - Authorization header: {auth_header[:50] if auth_header else 'None'}")
        
        if not auth_header:
            logger.info("JWT Auth - No authorization header")
            return None
        
        # Check for Bearer token format
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            logger.info(f"JWT Auth - Invalid format: {len(parts)} parts")
            return None
        
        token = parts[1]
        logger.info(f"JWT Auth - Token extracted: {token[:20]}...")
        
        try:
            user = get_user_from_token(token)
            logger.info(f"JWT Auth - User authenticated: {user.email}")
            return (user, None)
        except Exception as e:
            logger.error(f"JWT Auth - Error: {str(e)}")
            raise exceptions.AuthenticationFailed(str(e))
