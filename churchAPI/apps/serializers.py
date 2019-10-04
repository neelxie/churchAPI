from django.contrib.auth import authenticate

from rest_framework import serializers

class GoogleSerializer(serializers.Serializer):
    """
    This class implements serialization and deserialization of 
    for the facebook and google.
    """
    access_token = serializers.CharField(
        max_length=255, required=True, trim_whitespace=True)
    class Meta:
        model = User
        fields = ('access_token')