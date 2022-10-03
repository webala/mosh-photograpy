from rest_framework import serializers

class SetShootCompleteSerializer(serializers.Serializer):
    complete = serializers.BooleanField()