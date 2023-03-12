from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from wishlists.models import Wishlist


from .models import Perk, Experience

class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"

class PerkListSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "pk", "name", "details", "explanation"

class ExperienceDetailSerializer(ModelSerializer):

    host = TinyUserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    perks = PerkListSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_rating(self, experience):
        return experience.rating()
    def get_is_owner(self, experience):
        request = self.context['request']
        return experience.host == request.user
    def get_is_liked(self, experience):
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, experiences__pk=experience.pk).exists()

class ExperienceListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "perks",
            "is_owner",
            "is_liked",
        )
    def get_rating(self, experience):
        return experience.rating()
    def get_is_owner(self, experience):
        request = self.context['request']
        return experience.host == request.user
    def get_is_liked(self, experience):
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, experiences__pk=experience.pk).exists()
