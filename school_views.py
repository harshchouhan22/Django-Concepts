from rest_framework.views import APIView
from .school_models import *
from .serializers import *
from django.http import JsonResponse, status



class SchoolApis(APIView):
    def get(self, request):
        id = request.Get.get('id')
        if id:
            school = School.objects.get(id=id)
            serializers = SchoolSerializer(school)
            return JsonResponse({'data': serializers.data, 'status':status.HTTP_200_OK})
        else:
            school = School.objects.all()
            serializers = SchoolSerializer(school, many=True)
            return JsonResponse({'data': serializers.data, 'status': status.HTTP_200_OK})
    def post(self, request):
        data = request.data
        serializer = SchoolSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"data": serializer.data, 'status': status.HTTP_201_CREATED})
        else:
            return JsonResponse({'error': 'Something Went Wrong!', 'status': status.HTTP_500_BAD})
    
    def put(self, request):
        item = School.objects.get(id=request.data.id)
        if item:
            serializer = SchoolSerializer(request.data, optional=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data': serializer.data, 'status': status.HTTP_201_OK})            
            else:
                return JsonResponse({"error": 'something went Wrong!', status: status.HTTP_500_BAD})
        else:
            return JsonResponse({'error': 'School not found with this id', 'status': status.HTTP_404_NOT_FOUND})
    def delete(self, request):
        id = request.GET.get('id')
        if id:
            item = School.objects.get(id=id)
            item.delete()
            return JsonResponse({"message": 'School delete successfully!', 'status': status.HTTP_200_OK})
        else:
            return JsonResponse({'message': 'id is required!'})

#Api that uses, prefetch_related method, i want all the schools with avaliable classes in that
class PrefetchRelated(APIView):
    def get(self, request):
        try:
            school = School.objects.prefetch_related('school_classes').all()
            return JsonResponse({'data':school, 'status': status.HTTP_200_OK})
        except Exception as e:
            return JsonResponse({'message': 'Something went Wrong!', "error": str(e) })

#Api that uses prefetch_related method, i want all the exams results with students enrolled into it
class SelectRelated(APIView):
    def get(self, request):
        try:
            results = StudentResults.objects.select_related('student_results').all()
            return JsonResponse({'data': results, 'status': status.HTTP_200_OK})
        except Exception as e:
            return JsonResponse({'message': "Something Went Wrong!", 'status': status.HTTP_500_BAD})

#JWT Authentication
#Token Creation
import jwt
from django.contrib.auth import authenticate
from datetime import datetime, timedelta

def generate_token(user):
    duration = datetime.now() + timedelta(hours=12)
    if user:
        payload = {
            'username': user.username,
            'user_id': user.id,
            'exp': duration
        }
        token = jwt.encode(payload, 'settings.SECRET_KEY', algorithm='SH256') 
        return JsonResponse({'message': token('utf-8'), 'status': status.HTTP_200_OK})
    else:
        return JsonResponse({"message": 'user not found!'})


class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(data.username, data.password)
        if user is not None:
            token  = generate_token(user)
            return JsonResponse({'data': token, 'status': status.HTTP_200_OK})
        else:
            return JsonResponse({'message': 'user credentials were incorrect'})

#Authentication middleware
class Authentication(object):
    def __init__(self, role_type):
        self.role_type = role_type
    def wrapper(self, request):
        token = request.META.get('AUTHORIZATION_HEADER')
        if token:
            try:
                token_status = jwt.decode(token, 'settings.SECRET_KEY', algorithms='SHA256')
                user_id = token_status.get('user_id')
                user = Student.objects.get(id = user_id)
                if user.role == self.role_type:
                    return user
                else:
                    return JsonResponse({'message': 'Your Not Allowed To Access This Api!'})
            except jwt.ExpiredSignatureError:
                return JsonResponse({'message': 'Token Expired'})
            except jwt.InvalidSignatureError:
                return JsonResponse({'message': 'Invalid Token'})

@Authentication(role_type='Teacher')
def access_api_for_teacher(request):
    return "Access Granted"
        
from django.db.models import Q
#Student Search API
class SearchAPI(APIView):
    def get(self, request):
        query = request.GET.get('query')
        student = Student.objects.filter(Q(name__icontains = query) | Q(email__icontains = query) & ~Q(createdAt__lt = datetime.now()))

        return JsonResponse({"data": student, 'status': status.HTTP_200_OK})

from django.db.models import F, Avg, Sum, Count, Case, When, Value, IntegerField,Subquery, OuterRef, DateTimeField
#Dynamic Search 
class DynamicFilters(APIView):
    def get(self, request):
        #Subqueries, lets say i want to see student detail with its Exam instance
        exam_id = request.GET.data('exam_id')
        student_detail = Exam.objects.annotate(related_students = Subquery(Student.objects.get(id=OuterRef('student'))))
        all_the_exam_score_of_students = StudentResults.objects.filter(student__id='student_id').values('student__id').annotate(total_score=Sum('score'))
        student_count = Student.objects.all().count()

        student = Student.objects.filter(createdAt__lt = F('createdAt'))
        
        start_date = '2023-01-23'
        end_date = '2023-01-24'
        #Share me the list of students who is added in between 23 to 24
        students_2324 = Student.objects.filter(Q(createdAt__gte=start_date) | Q(createdAt__lt=end_date)).count()

        case = Student.objects.annotate(Case=When(createdAt='12-12-2023', then=Value(True)),
                                      default=Value(False),
                                      output_field = DateTimeField()).filter(is_created_today=True)




from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

# Lets Make Test Cases of School App
#tests / test_models.py
class SchoolModelTestCase(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='School1')
    
    def test_school_name(self):
        self.assertEqual(self.school.name, 'School1')

#tests / test_views.py
class SchoolViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_api_view(self):
        url = reverse('url-name')
        data = {'name': 'School'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.data['name'], 'School')


# Now Lets Build A Chat Function In between Student & Teacher
from channels.generic.websocket import AsyncWebsocketConsumer     
import json   
#group_add, group_discard, group_send, and send
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.connect()
        self.user = self.scope['user'].decode('utf-8')
        await self.channel_layer.group_add(
            self.user,
            self.channel_name
        )
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user,
            self.channel_name
        )

    async def receive(self, text_data):
        json_text_data = json.load(text_data)
        message = json_text_data['message']
        await self.channel_layer.group_send(
            self.user_id,
            {
                'type': 'chat.message',
                'message': message

            }
        )




