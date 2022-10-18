from rest_framework.routers import SimpleRouter

from lessons.views import LessonViewSet

router = SimpleRouter()
router.register('v1', LessonViewSet, basename='lesson')

urlpatterns = []
urlpatterns += router.urls
