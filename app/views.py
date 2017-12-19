from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Contact
from app.serializers import ContactSerializer


class LoginAPI(APIView):
    authentication_classes = []

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({'status': '0'})
        return Response({'status': '0',
                         'msg': 'bad session id'})

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return Response({'status': '0'})
        return Response({'status': '1',
                         'msg': 'username or password not valid'})


class RegisterAPI(APIView):
    authentication_classes = []

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        try:
            User.objects.get(username=username)
            return Response({'status': '1',
                             'msg': 'user already exits'})
        except User.DoesNotExist:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            return Response({'status': '0'})


class ContactsAPI(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'status': '-1',
                             'msg': 'please login at first!'})
        params = request.query_params
        if 'id' in params:
            id = params['id']
            id = int(id)
            type = params['type']
            if type == 'get':
                contact = Contact.objects.get(owner=user, id=id)
                serializer = ContactSerializer(contact)
                return Response({'status': '0',
                                 'contacts': serializer.data})
            elif type == 'delete':
                try:
                    contact = Contact.objects.get(id=id)
                    contact.delete()
                    return Response({'status': '0'})
                except Contact.DoesNotExist:
                    return Response({'status': '1',
                                     'msg': 'prime key is not valid'})
        else:
            contacts = Contact.objects.filter(owner=user)
            serializer = ContactSerializer(contacts, many=True)
            return Response({'status': '0',
                                 'contacts': serializer.data})

    def post(self, request):
        content = request.data
        type = content['type']
        data = content['contact']
        data['owner'] = request.user.id
        if type == 'add':
            number = Contact.objects.filter(id=request.user.id, name=data['name']).count()
            if number != 0:
                return Response({'status': '1',
                                 'msg': 'contact aleady exists'})
            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': '0',
                                 'type': 'add',
                                 'data': serializer.data})
        elif type == 'modify':
            id = data['id']
            name = data['name']
            contact = Contact.objects.get(id=id, name=name)
            serializer = ContactSerializer(contact, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': '0',
                                 'type': 'modify',
                                 'data': serializer.data
                                 })
        return Response({'status': '1',
                         'msg': 'data not valid'})


class LogoutAPI(APIView):
    def get(self, request):
        auth.logout(request)
        return Response({'status': '0'})
