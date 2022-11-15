from django.urls import path

from accounts.views import AccountRetrieve

urlpatterns = [
    path('', AccountRetrieve.as_view(), name='user_detail'),
]
