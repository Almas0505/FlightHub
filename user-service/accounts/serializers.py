"""
User serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'date_of_birth'
        ]
    
    def validate(self, data):
        """Validate passwords match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match'
            })
        return data
    
    def validate_email(self, value):
        """Check email uniqueness"""
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError('Email already registered')
        return value.lower()
    
    def validate_username(self, value):
        """Check username uniqueness"""
        if User.objects.filter(username=value.lower()).exists():
            raise serializers.ValidationError('Username already taken')
        return value.lower()
    
    def create(self, validated_data):
        """Create user"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate credentials"""
        email = data.get('email', '').lower()
        password = data.get('password')
        
        if not email or not password:
            raise serializers.ValidationError('Email and password required')
        
        # Authenticate
        user = authenticate(username=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')
        
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username',
            'first_name', 'last_name',
            'phone', 'date_of_birth',
            'passport_number', 'nationality',
            'country', 'city',
            'loyalty_points', 'tier',
            'preferred_language', 'preferred_currency',
            'email_notifications', 'sms_notifications',
            'created_at', 'last_login_at'
        ]
        read_only_fields = [
            'id', 'loyalty_points', 'tier',
            'created_at', 'last_login_at'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer"""
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate passwords"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': 'Passwords do not match'
            })
        return data


class RefreshTokenSerializer(serializers.Serializer):
    """Refresh token serializer"""
    refresh_token = serializers.CharField()
