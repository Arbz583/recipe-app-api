"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        # password remove from get, also do not return when post or updat
        # set_password do not checks strength.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        # if you do not using hashing (set_password) for system then password would be stored in plaintext in database and authenticatin system get to trouble!
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        # updating all fiels except password
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

# a more generic serializer is used because it doesn't directly map to a Django model; instead, it handles authentication based on provided credentials.
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    # mask input only in browsable api not in swagger
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        # returns a dictionary of validated attributes
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        # authenticated user must pass to ObtainAuthToken view
        attrs['user'] = user
        return attrs
# cleaned data (contain type of fields and their char's numbers) and validated data (extra customize validation with validate method) checks with is_valid() and then store in validated_data
