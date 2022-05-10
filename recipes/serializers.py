from rest_framework import serializers

from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        exclude = ['user']


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        exclude = ['user']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Ingredient.objects.all()
    )

    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        queryset = Tag.objects.all()
    )

    class Meta:
        model = Recipe
        exclude = ('user',)


class RecipeDetailSerializer(RecipeSerializer):
    ingredients = serializers.PrimaryKeyRelatedField(
        many = True,
        read_only = True
    )

    tags = serializers.PrimaryKeyRelatedField(
        many = True,
        read_only = True
    )
