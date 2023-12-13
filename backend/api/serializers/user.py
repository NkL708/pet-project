# pylint: disable=too-few-public-methods
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "is_staff"]

    def validate_password(self, value: str) -> str:
        user_data = self.initial_data
        user = self.instance or User(**user_data)
        try:
            validate_password(value, user=user)
        except ValidationError as e:
            raise DRFValidationError(e.messages) from e
        return value

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
