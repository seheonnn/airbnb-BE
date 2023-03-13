from django.utils import timezone
from rest_framework import serializers
from .models import Booking

class CreateRoomBookingSerializer(serializers.ModelSerializer):

    # RoomBooking 만을 위한 serializer에서는 check_in out 필수임.
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = ("check_in", "check_out", "guests",)

    # validation 커스텀, 3 개중 하나라도 error 발생하면 .is_valid() false 발생
    # def validate_필드 이름
    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value # 성공하면 해당 value를 return하게 해야 함

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value

    # data는 딕셔너리임
    def validate(self, data):
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check in should be smaller than check out.")
        # ********************
        if Booking.objects.filter(
            room=self.context['room'],
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")
        return data

# 모두가 보는 booking
class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )

# 집 주인이 보는 booking

# experience booking
class CreateExperienceBookingSerializer(serializers.ModelSerializer):

    experience_time = serializers.DateTimeField

    class Meta:
        model = Booking
        fields = ("experience_time", "guests",)

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value