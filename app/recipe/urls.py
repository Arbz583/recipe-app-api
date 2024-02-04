"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]


# If you use SimpleRouter, it expects your viewset to have methods corresponding to the standard CRUD actions. If a method is missing for a particular action, you may encounter an error when attempting to access the corresponding endpoint.
# List Action (GET): Corresponds to the list method.
# Create Action (POST): Corresponds to the create method.
# Retrieve Action (GET): Corresponds to the retrieve method.
# Update Action (PUT): Corresponds to the update method.
# Partial Update Action (PATCH): Corresponds to the partial_update method.
# Delete Action (DELETE): Corresponds to the destroy method.
# If you're using DefaultRouter, the API root will automatically be included.The API root is an endpoint that returns a response containing hyperlinks to all the list views.
# also With DefaultRouter, the generated URL patterns include format suffix patterns by default. This means that clients can append a suffix like .json, .api, or .xml to the URLs to specify the desired response format.
