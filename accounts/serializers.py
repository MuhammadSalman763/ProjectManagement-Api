from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile


# ============================================================
# User Registration Serializer
# ============================================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    role = serializers.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        default='developer'
    )

    contact_number = serializers.IntegerField(
        required=False,
        allow_null=True
    )

    profile_picture = serializers.ImageField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'role',
            'contact_number',
            'profile_picture',
        ]
        read_only_fields = ['id']

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError(
                'Username should only contain alphanumeric characters.'
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Username already exists.'
            )

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Email already exists.'
            )

        return value

    def create(self, validated_data):

        role = validated_data.pop(
            'role',
            'developer'
        )

        contact_number = validated_data.pop(
            'contact_number',
            None
        )

        profile_picture = validated_data.pop(
            'profile_picture',
            None
        )

        password = validated_data.pop('password')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        Profile.objects.create(
            user=user,
            role=role,
            contact_number=contact_number,
            profile_picture=profile_picture
        )

        return user

    def to_representation(self, instance):

        profile = instance.profile

        request = self.context.get('request')

        if profile.profile_picture:

            picture_added = True

            if request:
                picture_url = request.build_absolute_uri(
                    profile.profile_picture.url
                )
            else:
                picture_url = profile.profile_picture.url

        else:

            picture_added = False
            picture_url = None

        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'role': profile.role,
            'contact_number': profile.contact_number,
            'profile_picture_added': picture_added,
            'profile_picture': picture_url,
        }


# ============================================================
# User Login Serializer
# ============================================================

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise serializers.ValidationError(
                'Invalid username or password.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'User account is disabled.'
            )

        refresh = RefreshToken.for_user(user)

        attrs['user'] = user
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)

        return attrs


# ============================================================
# User Logout Serializer
# ============================================================

class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField(
        required=True
    )

    def validate_refresh(self, value):

        try:
            RefreshToken(value)

        except Exception:
            raise serializers.ValidationError(
                'Invalid or expired refresh token.'
            )

        return value

    def save(self, **kwargs):

        refresh_token = self.validated_data['refresh']

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except Exception:
            raise serializers.ValidationError(
                'Invalid or expired refresh token.'
            )

        return {
            'message': 'User logged out successfully.'
        }