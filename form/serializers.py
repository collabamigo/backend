from rest_framework import serializers
from .models import Form, Response, TextResponse, FileResponse


class FormSerializer(serializers.ModelSerializer):
    skeleton = serializers.ChoiceField(choices=[])

    class Meta:
        model = Form
        fields = ("id", "confirmation_message", "createdAt", "updatedAt",
                  "collect_email", "competition", "skeleton")
        read_only_fields = ("id", "confirmation_message", "createdAt",
                            "updatedAt", "collect_email", "competition",
                            "skeleton")


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ("form", "responders")
        read_only_fields = ("responders",)


class TextResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TextResponse
        fields = ("parent", "question_id", "value",)


class FileResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileResponse
        fields = ("parent", "question_id", "value")
