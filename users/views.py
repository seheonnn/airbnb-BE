from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound

from rooms.models import Room
from rooms.serializers import RoomListSerializer
from reviews.models import Review
from reviews.serializers import UserReviewSerializer
from . import serializers
from .models import User

# api/v1/users/me
class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            new_user = serializer.save()
            serializer = serializers.PrivateUserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# api/v1/users
class Users(APIView):
    def post(self, request): # ModelSerializer가 uniquness 보장해주기 때문에 pw에 대한 validation만 하면 됨
        password = request.data.get('password')
        if not password:
            raise ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data) # 해당 serializer에는 pw 포함 X
        if serializer.is_valid():
            # user.password = password # 이렇게 하면 raw pw가 그대로 DB에 들어감
            user = serializer.save()
            user.set_password(password) # pw hash화
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# api/v1/users/@seheon
class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExsists:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

# api/v1/users/change-password
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not old_password or not new_password:
            raise ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError

# api/v1/users/log-in
class LogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password) # username, password가 일치하면 user 반환
        if user:
            login(request, user) # user 정보가 담긴 session 생성, 사용자에게 cookie를 보내줌
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "wrong password"})


# api/v1/users/log-out
class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'pk': 'bye!'})


# api/v1/users/@seheon/rooms
class ShowRooms(APIView):
    def get(self, request, username):
        rooms = Room.objects.filter(owner__username=username)
        if rooms:
            serializer = RoomListSerializer(rooms, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            raise ParseError(f"{username} does not have any rooms.")

# api/v1/users/@seheon/reviews
class ShowReviews(APIView):
    def get(self, request, username):
        reviews = Review.objects.filter(user__username=username)
        if reviews:
            serializer = UserReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        else:
            raise ParseError(f"{username} does not have any reviews.")