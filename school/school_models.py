from django.db import models
import random, string

class School(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    school_code = models.CharField(unique=True)
    logo = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name +  " " + self.address
    
    class Meta:
        indexes = [models.Index(fields=['name', 'description'])]

    def save(self, *args, **kwargs):
        if not self.school_code:
            name_prefix = self.name[:2].upper()
            numbers_suffix = ''.join(random.choices(string.digits, k=4))
            self.school_code = name_prefix + numbers_suffix
        super(School, self).save(*args, **kwargs)

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    student_id = models.CharField(max_length=10, unique=True)
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=6)
    country = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name + " " + self.email

    class Meta:
        indexes = [models.Index(fields = ['name', 'email'])]

    def save(self, *args, **kwargs):
        name = self.name[:2].upper()
        numbers_suffix = ''.join(random.choices(string.digits, k=4))
        self.student_id = name + numbers_suffix
        super(Student, self).save(*args, **kwargs)

class Classes(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_classes')
    students = models.ManyToManyField(Student, on_delete=models.CASCADE, related_name='class_students')

    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now = True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='exam')

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    def __init__(self):
        return self.name
    
    class Meta:
        unique_together = ['name', 'classes']

class StudentResults(models.Model):
    score = models.IntegerField()
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_results')
    def __init__(self):
        return self.student.name +  self.exam.name

