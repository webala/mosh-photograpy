from rest_framework import serializers

class SetShootCompleteSerializer(serializers.Serializer):
    complete = serializers.BooleanField()

class MyMessageSerializer(serializers.Serializer):
    my_message = serializers.CharField()
    message_id = serializers.IntegerField()