from rest_framework.generics import ListAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from accounts.serializers import AccountSerializer


class AccountRetrieve(ListAPIView, UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(id=user.id)

    def get_object(self):
        user = self.request.user
        return get_object_or_404(self.queryset, id=user.id)

# class AccountPasswordUpdate(UpdateAPIView, ):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         user = self.request.user
#         return self.queryset.get_object_or_404(id=user.id)
