from django.db import models

# Create your models here.
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_student = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Team(models.Model):
    name = models.CharField(max_length=100)


class Student(models.Model):

    email = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,

    )

    college = models.CharField(max_length=300)
    linkedin = models.CharField(max_length=300)
    github = models.CharField(max_length=300)
    team = models.CharField(max_length=300, blank=True)


class mentor(models.Model):

    email = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,

    )
    team = models.CharField(max_length=300)
    linkedin = models.CharField(max_length=300)
# class StudentManager(BaseUserManager):

#     def create_student(self, first_name, last_name, email, qualification, university, password=None):
#         if email is None:
#             raise TypeError('Users must have an email address.')
#         student = Student(first_name=first_name, last_name=last_name,
#                           email=self.normalize_email(email),
#                           qualification=qualification, university=university)
#         student.set_password(password)
#         student.save()
#         return student


# class EmployeeManager(BaseUserManager):

#     def create_employee(self, first_name, last_name, email, designation, company, password=None):
#         if email is None:
#             raise TypeError('Users must have an email address.')
#         employee = Employee(first_name=first_name, last_name=last_name,
#                             email=self.normalize_email(email),
#                             designation=designation, company=company)
#         employee.set_password(password)
#         employee.save()
#         return employee


# class Student(CustomUser, PermissionsMixin):
#     qualification = models.CharField(db_index=True, max_length=255)
#     university = models.CharField(db_index=True, max_length=8)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name', 'university']


#     def __str__(self):
#         return self.first_name


# class Employee(CustomUser, PermissionsMixin):
#     designation = models.CharField(db_index=True, max_length=255)
#     company = models.CharField(db_index=True, max_length=255)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name', 'company']

#     objects = EmployeeManager()

#     def __str__(self):
#         return self.first_name
