# Lets Make a RoadMap for Simple Django Usage

from django.db import models
from rest_framework.views import APIView
from rest_framework import serializers
from django.http import JsonResponse, status
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
import jwt
from django.conf import settings
import json
import User, Q

class School(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    code = models.CharField(max_length=6, unique=True)
    contact = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    state = models.CharField(max_lenth=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField(max_length=6)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name + self.address
    
    class Meta:
        indexes = [models.Index(fields=['name'])]

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    dob = models.DateField()
    address = models.CharField(max_length=100)
    state = models.CharField()
    city = models.CharField()
    zipcode = models.IntegerField(max_length=6)
    joined_data = models.DateField()
    is_active = models.BooleanField()
    school = models.ForeignKey(School, on_delete = models.SET_NULL, related_name = 'student_school')

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name + self.email

    class Meta:
        indexes = [models.Index(fields=['name', 'email'])]

class Classes(models.Model):
    no = models.IntegerField(max_length=200)
    name = models.CharField(max_length=100)
    room_no = models.IntegerField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school')
    students = models.ManyToManyField(Student, on_delete= models.CASCADE, related_name='class_students')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name + ' its Room Number is ' + self.room_no

    class Meta:
        unique_together = [['room_no', 'school']]
        indexes =  [models.Index(fields=['name'])]

class Exams(models.Model):
    no = models.IntegerField(max_length=200)
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='exam_classes')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class StudentResults(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    exams = models.ForeignKey(Exams, on_delete= models.CASCADE)
    score = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.student.name + self.exams.name + self.score

# CRUD of School
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields= '__all__'
        
class SchoolWithStudentsSerializers(serializers.ModelSerializer):
    school_students = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = School
        fields = '__all__'


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

#JWT Authentication System


#LoginFunction
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    #Authenticate User
    user = authenticate(username=username, password=password)
    if user is not None:
        #Generate Token
        token = generate_token(user)
        user = User.objects.get(username = username)
        user.accessToken(token)
        user.save()
        return JsonResponse({'token': token, status: status.HTTP_200_OK})
    else:
        return JsonResponse({'error': 'Invalid Credentials'}, status = 401)

def generate_token(user):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': expiration_time,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algrothim='HS256')
    return token.decode('utf-8')

#Authentication System for Multiple users
class Authentication(object):
    def __init__(self, role_type):
        self.role_type = role_type
    def wrapper(self, request):
        token = request.META.get('AUTHORIZATION_HEADER')
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms='[SH256]')
                user_id = payload.get('user_id')
                if user_id:
                    user = User.objects.get(id=user_id)
                    if user.role == self.role_type:
                        return user
                    else:
                        return JsonResponse({"message": "user not found"})
            except jwt.ExpiredSignatureError:
                return JsonResponse({'message': 'Jwt token expired!'})
            except jwt.InvalidTokenError:
                return JsonResponse({'message': 'jwt token Invalid'})

@Authentication(role_type='Admin')
class SchoolAPIs(APIView):
    def get(self, request):
        id = request.GET.get('id')
        if id:
            school = School.objects.get(id=id)
            serializer = SchoolSerializer(school)
            return JsonResponse({'data': serializer.data, 'status': status.HTTP_200_OK})
        else:
            schools = School.objects.all()
            serializer = SchoolSerializer(schools, many=True)
            return JsonResponse({'data': serializer.data, 'status': status.HTTP_200_OK})
    
    def post(self, request):
        serializer = SchoolSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data, 'status': status.HTTP_200_OK})
        else:
            return JsonResponse({'data': serializer.data, 'status': status.HTTP_200_BAD})
        
    def put(self, request):
        serializer = SchoolSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data, 'status': status.HTTP_200_OK})
        else: 
            return JsonResponse({'data': serializer.data,'status': status.HTTP_200_BAD})
        
    def delete(self, request):
        id = request.GET.get('id')
        if id:
            school = School.objects.get(id=id)
            school.delete()
            return JsonResponse({'status': status.HTTP_200_OK})
        else:
            return JsonResponse({'status': status.HTTP_200_BAD})


#User prefetch Related, i want classes with its students
class PreFetchRelated(APIView):
    def get(self, request):
        classes = Classes.objects.prefetch_related('class_students')
        return JsonResponse({'data': classes, 'status':status.HTTP_200_OK})

#SelectRelated, i want all the students with their schools
class SelectedRelated(APIView):
    def get(self, request):
        students = Student.objects.select_related('schools')
        return JsonResponse({'data': students, 'status':status.HTTP_200_OK})

#Search bar
class Search(APIView):
    def get(self, request):
        query = request.GET.get('query')
        if query:
            schools = School.objects.filter(Q(name__icontains= query) | Q(address__icontains= query))
            serializers = SchoolSerializer(schools, many=True)
            return JsonResponse({'data': serializers.data, 'status':status.HTTP_200_OK})
        else:
            return JsonResponse({'status': status, 'message': 'query is required'})

#Chat Function( Using Django Channels)
from channels.generic.websocket import AsyncWebsocketConsumer

#Connect, diconnect, receive
class ConsumerChat(AsyncWebsocketConsumer):
    async def connect(self):
        #Accept the websocket connection
        await self.accept()
        self.user_id = self.scope['query_string'].decode('utf-8')
        # Add the Websocket connection to a group based on the user identifier
        await self.channel_layer.group_add(
            self.user_id,
            self.channel_name
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_id,
            self.channel_name
        )

    async def receive(self, text_data):
        #Receive a message from one participant and send it to the other
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.user_id,
            {
                'type': 'chat.message',
                'message': message
            }
        )
    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


#Testing: tests.py

from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse

#tests / test_models.py
class SchoolModelTestCase(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='School1')
    
    def test_school_name(self):
        self.assertEqual(self.school.name, 'School1')

#tests / test_views.py
        

class SchoolViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_school_api_view(self):
        url = reverse('school-create')
        data = {'name': 'New School'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 1)
        self.assertEqual(response.data['name'], 'New School')

#Django Signals, it has the following methods:- 
# 1. m2m_changed :- sent when a ManyToManyField in a model changes
# 2. pre_init and post_init :- sent before and after an instance's '__init__' method is called
# 3. pre_save and post_save :- signals are sent before and after the modle's save() method is called
# 4. request_started and request_finished :- Sent when a django request is started and finished.
# 5. user_logged_in and user_logged_out :- sent's when a user logs in or logs out
# 6.  django.db.backend.signals :- provides signals related to db operations, such as 'connection_created' which is sent after the connection is created.

from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver

@receiver(post_save, model=School)
def school_saved(sender, instance, **kwargs):
    print(f'This function will be called whenever school gets created')

@receiver(pre_delete, model=School)
def school_deleted(sender, instance, **kwargs):
    print(f"Article '{instance.title}' is about to be deleted")


#Editing Admin Dashboard
from django.contrib import admin
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'address')
    search_fields = ('name', 'email')

admin.site.register(School, SchoolAdmin)

# Django ORM: Advanced Querying:
from django.db.models import F, Avg, Sum, Count, Case, When, Value, IntegerField,Subquery, OuterRef

class AdvanceQueries(APIView):
    def get(self, request):
        # Case -insensitive search
        School.objects.filter(name__icontains='query')
        # Starts with
        School.objects.filter(name__startswith='prefix')
        # Ends with
        School.objects.filter(name__endswith='suffix')
        # Complex queries
        School.objects.filter(Q(name__icontains='query') | Q(description__icontains='query') & Q(createdAt__icontains=datetime.now()))
        # Using F Object, when you wnat to filter objects on a comparison between two fields without having to fetch the values and compare them.
        School.objects.filter(createdAt__gt=F('other_tables_createdAt')) 
        #Basic Aggregation:
        StudentResults.objects.aggregate(avg_score=Avg('score'), total_score=Sum('score'))
        #Group By
        StudentResults.objects.values('exam').annotate(count=Count('exam'))
        #Annotations
        StudentResults.objects.annotate(total=F('quantity') * F('price'))
        #Conditional Annotations:
        StudentResults.objects.annotate(
            discount=Case(
                When(quantity__gt=10, then=Value(0.1)),
                default=Value(1),
                output_field=IntegerField()
            )
        )
        #Subqueries:
        students_with_result = Student.objects.annotate(max_related=Subquery(StudentResults.objects.filter(student=OuterRef('id'))).values('value')[:1])
        #Lets say a question , Share me the name of students whose results are greater then 80
        students = Student.objects.filter(results__score__gt=80)
        # for Less than 40
        students_lessthen_40 = Student.objects.filter(results__score__lt = 40)
        # students = Student.objects.filter(results__attribute='some_value')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflow',
    }
}

from django.views.decorators.cache import cache_page, cache_control
from django.core.cache import cache
#Cache many have to methods set (with 3 paramenters) and get(with key) 
@cache_page(60 * 15) #Cache for 15 Minutes
def my_view(request):
    return "pass"

#Cache-control
@cache_control(max_age=3600)
def my_view(request):
    return "pass"

def my_view(request):
    #try to get data fom the cache
    data = cache.get('my_key')
    if data:
        data = "Harsh"
        cache.set('my_key', data, timeout=3600) #Cache for one hour






