"""
User views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils import timezone
import logging

from .models import UserProfile
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    ChangePasswordSerializer,
    RefreshTokenSerializer
)
from .jwt_auth import create_tokens, verify_token, create_access_token

User = get_user_model()
logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """User API ViewSet"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['register', 'login', 'refresh_token']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register new user
        
        POST /users/register/
        {
            "email": "user@example.com",
            "username": "username",
            "password": "securepass123",
            "password_confirm": "securepass123",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+77001234567"
        }
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = serializer.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Generate tokens
            tokens = create_tokens(user)
            
            logger.info(f"User {user.email} registered successfully")
            
            return Response({
                'user': UserSerializer(user).data,
                **tokens
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"User registration failed: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Registration failed', 'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        User login
        
        POST /users/login/
        {
            "email": "user@example.com",
            "password": "securepass123"
        }
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login_at = timezone.now()
        user.save()
        
        # Generate tokens
        tokens = create_tokens(user)
        
        logger.info(f"User {user.email} logged in")
        
        return Response({
            'user': UserSerializer(user).data,
            **tokens
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """
        Get current user profile
        
        GET /users/profile/
        Authorization: Bearer <token>
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """
        Update current user profile
        
        PUT/PATCH /users/update_profile/
        Authorization: Bearer <token>
        """
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        logger.info(f"User {request.user.email} updated profile")
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        Change user password
        
        POST /users/change_password/
        {
            "old_password": "oldpass123",
            "new_password": "newpass123",
            "new_password_confirm": "newpass123"
        }
        """
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        # Check old password
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Old password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        logger.info(f"User {user.email} changed password")
        
        return Response({'message': 'Password changed successfully'})
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh_token(self, request):
        """
        Refresh access token
        
        POST /users/refresh_token/
        {
            "refresh_token": "..."
        }
        """
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Verify refresh token
            payload = verify_token(serializer.validated_data['refresh_token'])
            
            if payload.get('type') != 'refresh':
                raise Exception('Invalid token type')
            
            # Get user
            user = User.objects.get(id=payload['user_id'])
            
            # Create new access token
            access_token = create_access_token(user)
            
            return Response({
                'access_token': access_token,
                'token_type': 'bearer',
            })
        
        except Exception as e:
            logger.error(f"Token refresh failed: {str(e)}")
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def loyalty_info(self, request):
        """
        Get loyalty program information
        
        GET /users/loyalty_info/
        """
        user = request.user
        
        # Calculate points to next tier
        tier_thresholds = {
            'BRONZE': 0,
            'SILVER': 10000,
            'GOLD': 25000,
            'PLATINUM': 50000,
        }
        
        current_threshold = tier_thresholds[user.tier]
        next_tier = None
        points_to_next = None
        
        tier_order = ['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']
        current_index = tier_order.index(user.tier)
        
        if current_index < len(tier_order) - 1:
            next_tier = tier_order[current_index + 1]
            next_threshold = tier_thresholds[next_tier]
            points_to_next = next_threshold - user.loyalty_points
        
        return Response({
            'loyalty_points': user.loyalty_points,
            'tier': user.tier,
            'next_tier': next_tier,
            'points_to_next_tier': points_to_next,
            'tier_benefits': self._get_tier_benefits(user.tier)
        })
    
    def _get_tier_benefits(self, tier):
        """Get benefits for tier"""
        benefits = {
            'BRONZE': [
                'Earn 1 point per 100 KZT spent',
                'Email support',
            ],
            'SILVER': [
                'Earn 1.5 points per 100 KZT spent',
                'Priority email support',
                '10% discount on baggage',
            ],
            'GOLD': [
                'Earn 2 points per 100 KZT spent',
                'Priority check-in',
                '20% discount on baggage',
                'Free seat selection',
            ],
            'PLATINUM': [
                'Earn 3 points per 100 KZT spent',
                'Priority check-in and boarding',
                'Free baggage',
                'Free seat selection',
                'Lounge access',
                'Free flight changes',
            ],
        }
        return benefits.get(tier, [])
