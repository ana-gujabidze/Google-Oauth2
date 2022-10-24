from rest_framework import serializers


class LoginInputSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    redirect_uri = serializers.CharField(required=True)
    ref_name = "login_serializer"


class RefreshInputSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    ref_name = "refresh_serializer"
