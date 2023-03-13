from django.conf import settings
from django.db import transaction
from django.utils import timezone

from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from categories.models import Category
from reviews.serializers import ReviewSerializer
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer
from bookings.serializers import CreateExperienceBookingSerializer
from .models import Perk, Experience
from .serializers import PerkSerializer, ExperienceListSerializer, ExperienceDetailSerializer


# api/v1/experiences/perks
class Perks(APIView):
    def get(self, request):
        all_Perks = Perk.objects.all()
        serializer = PerkSerializer(all_Perks, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(PerkSerializer(perk).data)
        else:
            return Response(serializer.errors)


# api/v1/experiences/perks/1
class PerkDetail(APIView):
    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound
    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)
    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)
    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)

# api/v1/experiences/experiences
class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(all_experiences, many=True, context={"request":request})
        return Response(serializer.data)
    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")  # category id를 user에서 넘겨주면
            if not category_pk:
                raise ParseError("Category is required")
            try:
                category = Category.objects.get(pk=category_pk)  # 해당 id로 category object 찾음
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be experiences")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    experience = serializer.save(host=request.user, category=category)
                    perks = request.data.get("perks")
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                    serializer = ExperienceDetailSerializer(experience, context={"request":request})
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Perk not found")
        else:
            return Response(serializer.errors)


# api/v1/experiences/1
class ExperiencesDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = ExperienceDetailSerializer(experience, context={"request":request})  # context= 를 통해 데이터를 직접 넘길 수도 있음
        return Response(serializer.data)
    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied

        serializer = ExperienceDetailSerializer(experience, data=request.data, partial=True)

        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    updated_experience = serializer.save(category=category)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("The category kind should be experiences")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")
            else:
                updated_experience = serializer.save()
            try:
                with transaction.atomic():
                    perks = request.data.get("perks")
                    if perks:
                        updated_experience.perks.clear()
                        for perk_pk in perks:
                            perk = Perk.objects.get(pk=perk_pk)
                            updated_experience.perks.add(perk)
                    serializer = ExperienceDetailSerializer(updated_experience, context={"request":request})
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Perk not found")
    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)

# api/v1/experiences/1/reviews
class ExperienceReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            return NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get('page', 1)
            page = int (page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        serializer = ReviewSerializer(experience.reviews.all()[start:end], many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(user=request.user, experience=self.get_object(pk))
            serializer = ReviewSerializer(review)
            return Response(serializer.data)

# api/v1/experiences/1/perks
class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            return NotFound
    def get(self, request, pk):
        try:
            page = request.query_params.get('page', 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        experience = self.get_object(pk)
        serializer = PerkSerializer(experience.perks.all()[start:end], many=True)
        return Response(serializer.data)

# api/v1/experiences/1/bookings
class ExperienceBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now())
        # print(now)
        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gte=now,
        )
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data, context={"experience":experience})
        if serializer.is_valid():
            booking =serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)