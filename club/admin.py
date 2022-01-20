from django.contrib import admin
from .models import Club, Competition, Announcement, CompetitionWinner


class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image_links", "college", "join_date",
                    "instagram", "linkedin", "facebook", "discord", "github", "mail", "telegram", "other",
                    "memberSize", )


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description",
                    "disabled", "image_links", "graph_link", "priority")


class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'club')


class CompetitionWinnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'competition', 'winner', 'position', 'index')


admin.site.register(Club, ClubAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Announcement, AnnouncementsAdmin)
admin.site.register(CompetitionWinner, CompetitionWinnerAdmin)
