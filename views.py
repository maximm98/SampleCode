import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from .serializers import NodeSerializer
from F5.models import Node
from libs import getF5Data
from .permissions import IsInGroup

logger = logging.getLogger(__name__)

# GET's the detail of nodes based on partition -> group user is in RBAC. .


class NodeListView(ListAPIView):
    permission_classes = [IsAuthenticated & IsInGroup]
    serializer_class = NodeSerializer
    queryset = Node.objects.all()

    def get(self, request, format=None):

        requestGroup = self.request.query_params.get('groups')
        if(requestGroup != 'admin'):
            queryset = Node.objects.filter(partition__iexact=requestGroup)
            serializer = NodeSerializer(queryset, many=True)
            return Response(serializer.data)

        elif(requestGroup == 'admin'):
            nodes = Node.objects.all()
            serializer = NodeSerializer(nodes, many=True)
            return Response(serializer.data)
        else:
            content = {'status': 'Insufficient Permissions'}
            status = '403'
            return Response(content, status)


# Imports Data from the F5 Load Balancer's defined in getF5Data(). 
class ImportData(ListAPIView):
    permission_classes = [IsAuthenticated & IsInGroup]
    serializer_class = NodeSerializer
    queryset = Node.objects.all()

    def get(self, request, format=None):

        requestGroup = self.request.query_params.get('groups')
        if(requestGroup == 'admin'):
            getF5Data.insertNodeTable()
            queryset = Node.objects.all()
            serializer = NodeSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            content = {'status': 'Insufficient Permissions'}
            status = '403'
            return Response(content, status)

# GET's the detail of nodes based on partition -> group user is in RBAC.


class NodeDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated & IsInGroup]
    serializer_class = NodeSerializer
    queryset = Node.objects.all()

    def get(self, request, format=None):
        requestGroup = self.request.query_params.get('groups')
        if(requestGroup != 'admin'):
            queryset = Node.objects.filter(partition__iexact=requestGroup)
            serializer = NodeSerializer(queryset, many=True)
            return Response(serializer.data)

        elif(requestGroup == 'admin'):
            queryset = Node.objects.all()
            return Response(queryset.data)

        else:
            content = {'status': 'Insufficient Permissions'}
            status = '403'
            return Response(content, status)

# PATCH's & GET's the state of a Node based on user input from the frontend.


class UpdateNodeStateView(UpdateAPIView):
    permission_classes = [IsAuthenticated & IsInGroup]
    queryset = Node.objects.all()
    serializer_class = NodeSerializer

    def patch(self, request, *args, **kwargs):
        # How we can get the data response, and then use this data to update F5. We can do some conditional statements based on this.
        kwargs['partial'] = True
        partial = kwargs
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        requestData = serializer.data
        requestGroup = request.data['groups']
        requestUsername = request.data['username']
        if(requestData['partition'].upper() == requestGroup.upper()):
            getF5Data.UpdateNodeState(
                requestData['vipname'], requestData['partition'], requestData['poolname'], requestData['nodename'], requestData['nodestate'])
            # Prints out:{'nodename': 'sadsad', 'partition': 'sadjfh', 'ipaddress': 'dsjfhl', 'nodestate': 'up', 'poolname': 'sdfjlkh', 'vipname': 'none', 'fqn': 'WTEDYGSADGKD', 'currentconnections': 90}
            return self.partial_update(request, *args, **kwargs)
        elif(requestGroup == 'admin'):
            getF5Data.UpdateNodeState(
                requestData['vipname'], requestData['partition'], requestData['poolname'], requestData['nodename'], requestData['nodestate'])
            # Prints out:{'nodename': 'sadsad', 'partition': 'sadjfh', 'ipaddress': 'dsjfhl', 'nodestate': 'up', 'poolname': 'sdfjlkh', 'vipname': 'none', 'fqn': 'WTEDYGSADGKD', 'currentconnections': 90}
            return self.partial_update(request, *args, **kwargs)

        else:
            content = {'status': 'Insufficient Permissions'}
            status = '403'
            return Response(content, status)


# View for Token Authentication. Provides custom response parameters such as groups.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['groups'] = self.user.groups.values_list('name', flat=True)
        return data

# View for serializing the token pair into JSON based on MyTokenObtainPairSerializer. Not currently used, but could be in the future so adding it as a placeholder.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
