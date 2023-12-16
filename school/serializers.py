from rest_framework.serializers import Serializer
from .school_models import *


class SchoolSerializer(Serializer.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class StudentSerializer(Serializer.ModelSerializer):
    class Meta:
        model  = Student
        fields = '__all__'

class ClassSerializer(Serializer.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__'

class ExamSerializer(Serializer.ModelSerializer):
    classes = ClassSerializer(many=True, read_only=True)
    class Meta:
        model = Exam
        fields = '__all__' 

    def to_representation(self, instance):
        formatted_createdAt = self.instance.createdAt.strftime('%Y-%M-%D %H:%M:%S')
        representation = super().to_representation(instance)
        representation['createdAt'] = formatted_createdAt
        return representation
    


    