from django.urls import path, include

urlpatterns = [
    path('lessons/', include('lessons.urls')),
    path('user/', include('accounts.urls')),
    path('teacher-note/', include('teacher_note.urls'))
]
