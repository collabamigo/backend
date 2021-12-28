from rest_framework import routers
from . import views
from backend import settings

if settings.DEVELOPMENT:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register(r'ecell', views.IdeaView, 'ecell')
router.register(r'my-ideas', views.SelfIdeaView, 'self_ideas')

urlpatterns = [
]

urlpatterns += router.urls
