#hat are Different Model Inheritance styles in Django?
# 1. Abstract Base classes
# 2. Multi-table Inheritance
# 3. Proxy models


from django.db import models

##Abstract Base Classes:
# Explanation: Abstract base classes are used when you want to define a model that includes common fields and methods that can be shared among multiple other models. However, you don't intend to create database tables for the abstract base class itself.
# Usage: You define an abstract base class by setting abstract = True in the Meta class of the model. Other models can then inherit from this abstract base class, gaining its fields and methods without creating a separate table for the base class.
class MyBaseClass(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True
        ordering = ['name']
        verbose_name_plural = 'MyBaseClass'

class MyModel(MyBaseClass):
    description = models.TextField()


# #Multi-table Inheritance
# Explanation: Multi-table inheritance involves creating a new database table for the derived model, which includes all the fields from both the base model and the derived model. Each table is linked through a one-to-one relationship.
# Usage: To implement multi-table inheritance, you simply create a new model that inherits from an existing model.
class MyModel2(models.Model):
    name = models.TextField()

class MyModel3(MyModel2):
    description = models.TextField()

# #Proxy Models
# Explanation: Proxy models are used when you want to alter the behavior of an existing model without changing its fields. A proxy model uses the same database table as the original model but allows you to override some methods or add new methods.
# Usage: To create a proxy model, you define a new model with the Meta class attribute proxy = True.

class MyModel4(models.Model):
    name = models.TextField()

class MyModel4Proxy(MyModel4):
    class Meta:
        proxy = True
    
    def custom_method(self):
        #Custom logix here








