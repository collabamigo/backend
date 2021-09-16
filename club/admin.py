# from django.contrib import admin
# from .models import Club, Social, Competition, Entry, Choice, Form, Question,\
#     Answer, Response
#
#
# # Register your models here.
# class ClubAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "link", "picture", "college", "join_date",)
#
#
# class CompetitionAdmin(admin.ModelAdmin):
#     list_display = ("id", "club", "on_going",)
#
#
# class SocialAdmin(admin.ModelAdmin):
#     list_display = ("id", "club", "instagram", "linkedin", "facebook",
#                     "discord", "other")
#
#
# class EntriesAdmin(admin.ModelAdmin):
#     list_display = ("id", "participant", "competition",)
#
#
# class ChoicesAdmin(admin.ModelAdmin):
#     list_display = ("id", "choice", "is_answer",)
#
#
# class FormAdmin(admin.ModelAdmin):
#     list_display = ("id", "entries", "edit_after_submit",
#                     "confirmation_message", "is_quiz", "allow_view_score",
#                     "createdAt", "updatedAt", "collect_email",)
#
#
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ("id", "form_id", "question", "question_type", "required",
#                     "answer_key", "score", "choices",)
#
#
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ("id", "answer", "question",)
#
#
# class ResponseAdmin(admin.ModelAdmin):
#     list_display = ("id", "form", "responder_email", "response")
#
#
# admin.site.register(Club, ClubAdmin)
# admin.site.register(Social, SocialAdmin)
# admin.site.register(Competition, CompetitionAdmin)
# admin.site.register(Entry, EntriesAdmin)
# admin.site.register(Choice, ChoicesAdmin)
# admin.site.register(Form, FormAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Answer, AnswerAdmin)
# admin.site.register(Response, ResponseAdmin)
