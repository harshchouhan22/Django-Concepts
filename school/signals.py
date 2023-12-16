from django.dispatch import Signal, receiver 
from django.db.models.signals import pre_save, post_save, pre_delete, m2m_changed
from .school_models import *

@receiver(pre_save, sender=School)
def save_student(sender, instance, **kwargs):
    print('this function will work when student gets created!')

@receiver(post_save, sender=School)
def after_student_saved(sender, instance, **kwargs):
    print('This function will work after students will get created!')

@receiver(pre_delete, sender = School)
def before_student_delete(sender, instance, **kwargs):
    print('This function will work after student gets created!')

@receiver(m2m_changed, sender=Classes.students.through)
def changes_in_students(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']
        print('This function will gets print when ever any changes in students in a class')
