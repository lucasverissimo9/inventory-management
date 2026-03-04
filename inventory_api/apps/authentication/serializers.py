from django.contrib.auth import authenticate
from rest_framework import serializers
from apps.users.models import User
from apps.company.models import CompanyUserMembership
from common.exceptions import UserEmailNotFound

import logging

logger = logging.getLogger(__name__)

class AuthLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    logging.info("Requesting Auth Login")

    def validate(self, attributes):
        
        email = attributes["email"].lower().strip()
        password = attributes["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserEmailNotFound(email=email)

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user.status == "inactive":
            raise serializers.ValidationError("The user is inactive")

        attributes["user"] = user
        return attributes


class AuthRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    name = serializers.CharField(max_length=255)
    role = serializers.ChoiceField(
        choices=CompanyUserMembership.UserRole.choices,
        default=CompanyUserMembership.UserRole.MEMBER,
    )

    logging.info("Requesting Auth Register")

    def validate_email(self, value):
        if User.objects.filter(email=value.lower().strip()).exists():
            raise serializers.ValidationError("Email already registered.")
        return value.lower().strip()

    def validate_password(self, value):
        if value.isdigit() or value.isalpha():
            raise serializers.ValidationError(
                "Password must contain letters and numbers."
            )
        return value

    def create(self, validated_data):

        company = self.context["company"]  
        role = validated_data.pop("role")

        user = User.objects.create(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
        )
        CompanyUserMembership.objects.create(
            company=company,
            user=user,
            user_role=role,
        )
        return user