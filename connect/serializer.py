from rest_framework import serializers

from . models import Todo, Profile, Teacher, Skill


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed')


class TodoSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"

    def to_representation(self, instance):
        ret = super(TodoSerializer2, self).to_representation(instance)
        # check the request is list view or detail view
        is_list_view = isinstance(self.instance, list)
        extra_ret = {'id': '[1]'} if is_list_view else {
            'id': '1'}
        ret.update(extra_ret)
        return ret


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'age', 'gender',
                  'education', 'email', 'contact', 'handle', 'isvendor')


# class ProfileSerializer2(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('id')


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('id', 'Skill_set')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'Teacher_set')
