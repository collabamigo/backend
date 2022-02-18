from django.contrib import admin
from .models import Club, Competition, Announcement, CompetitionWinner, ClubMembership


class ClubAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "join_date", "instagram", "linkedin", "facebook",
                    "discord", "github", "mail", "telegram", "other", "memberSize",)


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active",
                    "image_links", "graph_link", "priority")


class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'club')


class CompetitionWinnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'competition', 'winner', 'position', 'index')


class ClubMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'club')


admin.site.register(Club, ClubAdmin)
admin.site.register(Competition, CompetitionAdmin)
admin.site.register(Announcement, AnnouncementsAdmin)
admin.site.register(CompetitionWinner, CompetitionWinnerAdmin)
admin.site.register(ClubMembership, ClubMembershipAdmin)
