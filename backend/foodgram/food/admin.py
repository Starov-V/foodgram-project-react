from django.contrib import admin
from .models import Tag, Ingredient, Recipe, IngredientRecipe, TagRecipe

admin.site.register(Tag)
admin.site.register(TagRecipe)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(IngredientRecipe)
