from rest_framework import serializers
from .models import Amenity, Room
from users.serializer import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer



# class RoomSerializer(ModelSerializer):
#     class Meta:
#         model = Room
#         fields = "__all__"
#         depth = 1 # owner에 userid가 들어가는 것이 아닌 user object가 들어감 -> 데이터가 너무 많아짐


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "name", "description"

class RoomDetailSerializer(serializers.ModelSerializer):

    owner = TinyUserSerializer(read_only=True)
    # amenities = AmenitySerializer(read_only=True, many=True) # amenity 여러 개 many= 추가
    category = CategorySerializer(read_only=True)

    # rating 값을 return하는 method를 만들 것임.
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField() # 인스타그램에서 is_liked(좋아요)로 사용, 값에 따라 빨간 하트, 빈 하트

    # reviews = ReviewSerializer(many=True, read_only=True)
    photos = PhotoSerializer(many=True, read_only=True)


    class Meta:
        model = Room
        fields = "__all__"
        # depth=1

    def get_rating(self, room): # 이름은 항상 'get_값 이름'
        print(self.context)
        return room.rating()

    def get_is_owner(self, room):
        request = self.context['request'] # context= 를 통해 넘어온 데이터 사용
        return room.owner == request.user

class RoomListSerializer(serializers.ModelSerializer): # 방에 대한 작은 정보들만 줌

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )
    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, room):
        request = self.context["request"]  # context= 를 통해 넘어온 데이터 사용
        return room.owner == request.user
