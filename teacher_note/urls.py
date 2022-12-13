from rest_framework.routers import SimpleRouter

from teacher_note.views import NoteViewSet

simpleRouter = SimpleRouter()
simpleRouter.register('v1',NoteViewSet,basename='notes')
urlpatterns = []
urlpatterns += simpleRouter.urls