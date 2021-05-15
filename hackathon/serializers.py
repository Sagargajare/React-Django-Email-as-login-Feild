from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from django.db.models import fields
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from .models import Student, CustomUser, mentor
from djoser import utils
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.dispatch import receiver  # add this
from django.db.models.signals import post_save  # add this
from .models import mentor as menterModels
from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage


class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ('email', )


class StudentsRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    students = StudentsSerializer(required=True, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = CustomUser
        fields = tuple(CustomUser.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
            'students'
        )

    def validate(self, attrs):

        user = CustomUser(
            email=attrs.get("email"),
            is_student=True,
            is_mentor=False,
            first_name=attrs.get("first_name"),
            last_name=attrs.get("last_name"),
        )
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop('students')
        try:
            user = self.perform_create(validated_data)

            Student = self.Student_create(user_data, validated_data, user)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():

            user = CustomUser.objects.create_user(
                email=validated_data.get("email"),
                is_student=True,
                is_mentor=False,
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("last_name"),
                password=validated_data.get("password"),
            )
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])

        return user

    def Student_create(self, user_data, validated_data, user):

        student = Student.objects.create(
            email=user,
            **user_data,

        )
        student.save()

        return None


class MentorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = mentor
        exclude = ('email', )


class MentorsRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    Mentors = MentorsSerializer(required=True,  write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = CustomUser
        fields = tuple(CustomUser.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            "password",
            'Mentors'

        )

    def validate(self, attrs):

        user = CustomUser(
            email=attrs.get("email"),
            is_student=False,
            is_mentor=True,
            first_name=attrs.get("first_name"),
            last_name=attrs.get("last_name"),
        )
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs

    def create(self, validated_data):
        user_data = validated_data.pop("Mentors")
        try:
            user = self.perform_create(validated_data)
            mentors = self.Mentors_create(user_data, validated_data, user)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():

            user = CustomUser.objects.create_user(
                email=validated_data.get("email"),
                is_student=False,
                is_mentor=True,
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("last_name"),
                password=validated_data.get("password"),
            )
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user

    def Mentors_create(self, user_data, validated_data, user):

        menter = menterModels.objects.create(
            email=user,
            **user_data,

        )
        menter.save()

        return None

# Custom Current User serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = tuple(CustomUser.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_student',
            'is_mentor',
        )
        read_only_fields = (settings.LOGIN_FIELD, 'is_student',
                            'is_mentor',)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(CustomUser)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)


class ActivationEmail(BaseEmailMessage):
    print("email backend hits 1")
    template_name = "email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        print(context)
        print("email backend hits")
        return context
