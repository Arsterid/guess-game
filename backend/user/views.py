from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.models import User
from user.serializers import UserSerializer


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @permission_classes([IsAuthenticated])
    @action(methods=['POST'], detail=False, description="Get current user data")
    def get_data(self, request):
        serializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

