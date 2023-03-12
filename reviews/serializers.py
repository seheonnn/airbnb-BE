from rest_framework import serializers
from .models import Review
from users.serializers import TinyUserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = TinyUserSerializer(read_only=True) # 리뷰 생성 시에 유저에게 유저 정보를 묻지 않고 알아서 가져오기 때문
    class Meta:
        model = Review
        fields = ("user", "payload", "rating")


class UserReviewSerializer(serializers.ModelSerializer):

    room_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ("room_name", "payload", "rating")

    def get_room_name(self, review):
        return review.room.name
