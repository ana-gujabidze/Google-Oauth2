from datetime import datetime

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .services import authenticate_user


class LoginView(APIView):

    class LoginInputSerializer(serializers.Serializer):
        code = serializers.CharField(required=True)
        redirect_uri = serializers.CharField(required=True)
        ref_name = "login_serializer"

    @swagger_auto_schema(request_body=LoginInputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.LoginInputSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            user = authenticate_user(code=data.get('code'), redirect_uri=data.get('redirect_uri'))
            jwt_token = RefreshToken.for_user(user)
            access_token = str(jwt_token.access_token)
            refresh_token = str(jwt_token)

            # Create payload
            payload = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }
            return Response(payload)
        return Response({
            'error': {
                'code': 'invalid_paramter',
                'message': f'Input validation error: {serializer.errors}'
            }
        }, status=status.HTTP_400_BAD_REQUEST)

class RefreshView(APIView):

    class RefreshInputSerializer(serializers.Serializer):
        refresh_token = serializers.CharField(required=True)
        ref_name = 'refresh_serializer'

    @swagger_auto_schema(request_body=RefreshInputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.RefreshInputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            jwt_token = RefreshToken(data['refresh_token'])
            user_id = jwt_token[api_settings.USER_ID_CLAIM]
            profile = Profile.objects.get(user_id=user_id)
            user = profile.user
            jwt_token = RefreshToken.for_user(user)
            access_token = str(jwt_token.access_token)
            refresh_token = str(jwt_token)

            # Create payload
            payload = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            }
            return Response(payload)
        return Response({
            'error': {
                'code': 'invalid_paramter',
                'message': f'Input validation error: {serializer.errors}'
            }
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        payload = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
        return Response(payload)
