from django.dispatch import Signal, receiver 
from django.db.models.signals import post_delete,  pre_save, post_save, pre_delete, m2m_changed
from .school_models import *
from django.contrib.auth.signals import user_logged_in, user_logged_out

# Pre-save and post-save for a different model:
@receiver(pre_save, sender=School)
def save_student(sender, instance, **kwargs):
    print('this function will work when student gets created!')

@receiver(post_save, sender=School)
def after_student_saved(sender, instance, **kwargs):
    print('This function will work after students will get created!')





# Pre-delete and post-delete for a different model:

@receiver(pre_delete, sender=Student)
def before_student_delete(sender, instance, **kwargs):
    print('This function will work before a student is deleted!')

@receiver(post_delete, sender=Student)
def after_student_deleted(sender, instance, **kwargs):
    print('This function will work after a student is deleted!')





#Signals for When Users-Logs in
@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    print(f"The user {user.username} has logged In!")

@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    print(f'The user {user.username} has logged out!')




# Signal for when a file is uploaded:
from django.core.files.storage import default_storage
class File(models.Model):
    file = models.FileField(upload_to='uploads/')

@receiver(post_save, sender=File)
def file_saved(sender, instance, created, **kwargs):
    if created:
        file_path = default_storage.url(instance.file.name)
        print(f'A new file has been updated: {file_path}')




#Signal for many-to-many relationship changes in a different model:
@receiver(m2m_changed, sender=Classes.students.through)
def changes_in_students(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']
        print('This function will gets print when ever any changes in students in a class')


