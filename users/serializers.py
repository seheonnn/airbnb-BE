from rest_framework import serializers

from .models import User

# room 정보를 볼 때 간단하게 보여줄 user 정보
class TinyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )

# 자신의 private한 정보
class PrivateUserSerializer(serializers.ModelSerializer):

    total_rooms = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )
    def get_total_rooms(self, user):
        return user.total_rooms()
    def get_total_reviews(self, user):
        return user.total_reviews()
