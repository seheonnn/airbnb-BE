from django.shortcuts import render
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied

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
    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceListSerializer(all_experiences, many=True, context={"request":request})
        return Response(serializer.data)
    def post(self, request):
        pass
# api/v1/experiences/experiences/1
class ExperiencesDetail(APIView):
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
        pass
    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)