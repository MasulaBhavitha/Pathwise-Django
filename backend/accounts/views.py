from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ensure_profile
from .serializers import ProfileUpdateSerializer, RegisterSerializer, UserSerializer


def tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {**tokens_for(user), "user": UserSerializer(user).data},
            status=201,
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ensure_profile(request.user)
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        profile = ensure_profile(request.user)
        serializer = ProfileUpdateSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)
