from datetime import datetime

from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from google_auth.models import Profile
from google_auth.serializers import LoginInputSerializer, RefreshInputSerializer
from google_auth.services import authenticate_user


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginInputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = authenticate_user(code=data.get("code"), redirect_uri=data.get("redirect_uri"))
        jwt_token = RefreshToken.for_user(user)
        access_token = str(jwt_token.access_token)
        refresh_token = str(jwt_token)

        # Create payload
        payload = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }
        return Response(payload)


class RefreshView(APIView):
    @swagger_auto_schema(request_body=RefreshInputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RefreshInputSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            jwt_token = RefreshToken(data["refresh_token"])
        except TokenError as e:
            raise ValidationError(e)
        user_id = jwt_token[api_settings.USER_ID_CLAIM]
        profile = Profile.objects.get(user_id=user_id)
        user = profile.user
        jwt_token = RefreshToken.for_user(user)
        access_token = str(jwt_token.access_token)
        refresh_token = str(jwt_token)

        # Create payload
        payload = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }
        return Response(payload)


class LoremIpsumView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "title": "Lorem Ipsum",
            "paragraph": """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut sed risus a ante euismod laoreet. Vestibulum vel congue ipsum. Proin tempus leo nunc. Nulla pellentesque porta tortor vitae tempus. Phasellus porttitor lacus sit amet lobortis dictum. In vel gravida augue, et vulputate purus. Fusce eu nulla sed velit ultrices pellentesque. Donec imperdiet purus orci, id vehicula ex elementum in. Ut nec neque a dolor semper pellentesque. In consectetur sapien a tortor blandit, ut cursus enim placerat. Duis ac quam sed nulla commodo ultrices. Phasellus laoreet convallis arcu, ut pulvinar nunc ornare a. Duis nec nulla in magna maximus pulvinar ut vitae tellus.

            Nam faucibus tincidunt mauris, et ultricies ipsum sollicitudin at. Fusce sapien lectus, porttitor id sapien vel, rhoncus varius orci. Sed a quam at urna fringilla dictum vel eget nulla. Duis tincidunt maximus efficitur. Nulla ultricies quam lectus, ac condimentum nunc ultrices quis. Maecenas lacinia semper sapien dictum pellentesque. Mauris tincidunt tempus neque, sit amet suscipit tortor convallis a. Vestibulum mattis metus et lacus blandit, sit amet viverra ligula finibus. Sed placerat tincidunt tortor quis eleifend. Nulla condimentum volutpat urna a tristique.

            Nullam congue non leo eu vehicula. Pellentesque finibus lobortis elit, eu auctor tortor cursus in. Quisque mattis id lorem eget aliquet. Suspendisse placerat lorem sed quam posuere bibendum. Sed vulputate sit amet est ac blandit. Mauris vehicula nisl sed lectus aliquet tristique. Aliquam venenatis ultrices imperdiet. Praesent sagittis sagittis ligula, sed porttitor lorem posuere in. Aenean convallis dui nisi, non rhoncus nulla condimentum a. Vestibulum aliquet arcu id magna efficitur placerat. Nam tempor accumsan ligula, hendrerit scelerisque erat molestie eu. Praesent eget hendrerit risus.

            Donec tortor massa, interdum in ligula in, dapibus placerat est. Etiam ac lectus sapien. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Duis ut orci rutrum, porttitor nibh a, auctor nisl. In eget ultrices mi. Nam erat purus, varius eget porttitor vel, tempus eget justo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Proin eu posuere odio. Pellentesque ante urna, gravida facilisis sagittis non, semper nec tortor.

            Donec id euismod orci, quis consectetur massa. Fusce sed purus non risus dignissim elementum at suscipit arcu. Donec tincidunt lacus a mi pulvinar, et volutpat odio efficitur. Sed ullamcorper et ex vitae iaculis. Integer id iaculis tortor. Phasellus suscipit elit neque, sit amet mollis velit sollicitudin vel. Nunc feugiat iaculis arcu, ac venenatis est lacinia ac. In felis metus, volutpat eu nibh nec, vulputate viverra nisl. Praesent sollicitudin iaculis sem, in sollicitudin odio tristique at. Aenean eu elementum nibh, a gravida neque. Sed vestibulum magna turpis, nec suscipit dolor ultricies vel. In feugiat leo lacus, eu cursus nisi commodo at.
            """,
        }
        return Response(data=data, status=status.HTTP_200_OK)
