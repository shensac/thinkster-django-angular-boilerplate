from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status

from thinkster_django_angular_boilerplate.authentication.models import Account
from thinkster_django_angular_boilerplate.authentication.permissions import \
    IsAccountOwner
from thinkster_django_angular_boilerplate.authentication.serializers import \
    AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        print 'in create'
        serializer = self.serializer_class(data=request.DATA)
        print request.DATA
        if serializer.is_valid():
            account = Account.objects.create_user(**request.DATA)
            account.set_password(request.DATA.get('password'))
            account.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print serializer.errors
        return Response({
                            'status': 'Bad request',
                            'message': 'Account could not be created with received data.'
                        }, status=status.HTTP_400_BAD_REQUEST)