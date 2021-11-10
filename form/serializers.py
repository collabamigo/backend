import json

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Form, Response, TextResponse, FileResponse


def uniqueness_check(temp_list: list, message: str):
    temp_set = set(map(str, temp_list))
    if len(temp_set) != len(temp_list):
        raise ValidationError(message)


def validate_skeleton_element(element: dict, id: int):
    valid_keys = ["name", "type", "id"]

    # Adding id
    element["id"] = id

    if not element.get("name"):
        raise ValidationError("A question does matter,I guess")

    elif element["type"] == "text":
        pass

    elif element["type"] == "textarea":
        pass

    elif element["type"] == "checkbox":
        if not element.get("options") or element.get("options") == "":
            raise ValidationError("Oops ! A question needs options")
        # elif len(element["options"].split(";")) < 1:
        #     raise ValidationError(
        #         "Oops ! An MCQ question needs to have more"
        #         " than one option")
        # elif element["options"] != "":
        #     uniqueness_check(list(element.keys()),
        #                      "Oops! There seems to be a"
        #                      " duplicate in the mcq")

        valid_keys += ["options"]

    elif element["type"] == "number":
        pass

    elif element["type"] == "radio":
        if not element.get("options") or element.get("options") == "":
            raise ValidationError("Oops ! A question needs options")
        # elif len(element["options"].split(";")) < 0:
        #     raise ValidationError(
        #         "Oops ! An SCQ question needs to have more"
        #         " than one option")
        # elif element["options"] != "":
        #     uniqueness_check(list(element.keys()),
        #                      "Oops! There seems to be a"
        #                      " duplicate in the scq")
        valid_keys += ["options"]

    elif element["type"] == "file":
        pass

    elif element["type"] == "date":
        pass

    elif element["type"] == "datetime-local":
        pass

    elif element["type"] == "time":
        pass

    elif element["type"] == "email":
        pass

    else:
        raise ValidationError("Invalid question type")

    return {k: v for (k, v) in element.items() if k in valid_keys}


class FormSerializer(serializers.ModelSerializer):

    def validate_skeleton(self, attrs):
        skeleton: list = json.loads(attrs)
        result = []
        for _ in range(len(skeleton)):
            result += [validate_skeleton_element(skeleton[_], _+1)]
        return json.dumps(result)

    class Meta:
        model = Form
        validators = []
        fields = ["id", "confirmation_message", "createdAt", "updatedAt",
                  "collect_email", "competition", "skeleton"]
        read_only_fields = ["id", "createdAt", "updatedAt"]


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
