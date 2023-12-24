# pylint: disable=too-few-public-methods
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DRFValidationError


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "is_staff"]

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs["password"]
        try:
            validate_password(password, user)
        except ValidationError as e:
            raise DRFValidationError({"password": e.messages}) from e
        return attrs

    def create(self, validated_data) -> User:
        user = User(**validated_data)
        password = validated_data.pop("password", None)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    # pylint: disable=abstract-method
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_new_password = serializers.CharField(
        write_only=True, required=False
    )

    def validate_email(self, email: str) -> str:
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist as exc:
            raise serializers.ValidationError(
                "Пользователь с указанным адресом электронной почты не найден."
            ) from exc
        return email

    def validate_passwords(self, data):
        password = data.get("new_password")
        confirm_password = data.get("confirm_new_password")
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data
