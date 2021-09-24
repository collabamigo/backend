from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Form, Response, TextResponse, FileResponse


def uniqueness_check(temp_list: list, message: str):
    temp_set = set(map(str, temp_list))
    if len(temp_set) != len(temp_list):
        raise ValidationError(message)


def validate_skeleton_element(element: dict):
    if not element["label"]:
        raise ValidationError("A question does matter,I guess")

    if element["type"] == "text":
        pass

    elif element["type"] == "mcq":
        if not element["label"]:
            raise ValidationError("Oops ! A question does matter")
        elif not element["choice"]:
            raise ValidationError("Oops ! A question needs options")
        elif len(element["choice"]) < 1:
            raise ValidationError("Oops ! An MCQ question needs to have more"
                                  " than one option")
        elif element["choice"] != "":
            uniqueness_check(list(element.keys()), "Oops! There seems to be a duplicate in the mcq")

    elif element["type"] == "integer":
        pass


class FormSerializer(serializers.ModelSerializer):

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
