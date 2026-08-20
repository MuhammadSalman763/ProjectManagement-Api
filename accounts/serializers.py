from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile


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