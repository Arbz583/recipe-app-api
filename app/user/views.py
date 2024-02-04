"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    # we do not have browsable api for this view (default only is Json)
    # When DEBUG is set to False, Django REST Framework automatically disables the Browsable API.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # retrieving the object that the view is operating on
    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

# instance = self.get_object() in RetrieveModelMixin. it is also pass to serializers in instance
# When you call serializer.save() in a DRF view, it internally calls the create or update method of the serializer, depending on whether you are creating or updating an instance. so create or update only occur if validation data pass succussfully
