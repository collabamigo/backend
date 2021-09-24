from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Form, Response, TextResponse, FileResponse


def validate_skeleton_element(element: dict):
    if not element["label"]:
        raise ValidationError("A question does matter,I guess")

    if element["type"] == "text":
        if not element["label"]:
            raise ValidationError("Oops ! A question does matter")

    if element["type"] == "mcq":
        if not element["label"]:
            raise ValidationError("Oops ! A question does matter")
        elif not element["choice"]:
            raise ValidationError("Oops ! A question needs options")
        elif len(element["choice"]) < 1:
            raise ValidationError("Oops ! An MCQ question needs to have more"
                                  " than one option")
        elif element["choice"] != "":
            temp_list = element.keys()
            temp_set = set(map(str, temp_list))
            if len(temp_set) != len(temp_list):
                raise ValidationError("Oops! There seems to be a duplicate"
                                      " in the mcq")

    if element["type"] == "integer":
        if not element["label"]:
            raise ValidationError("A question does matter,I guess")

    # if element["type"] == "email":
    #     email_validator = EmailValidator(message="Please enter a correct Email address")
    #     email_validator(element["value"])


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
