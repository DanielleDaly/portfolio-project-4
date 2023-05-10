from . import views
from django.urls import path

urlpatterns = [
    path('', views.RecipeList.as_view(), name='home'),
    path('<slug:slug>/', views.FullRecipe.as_view(), name='full-recipe'),
    path('like/<slug:slug>', views.RecipeLike.as_view(), name='recipe_like'),
]

