from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from itez.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "is_active", "date"]

    def create(self, validated_data):

        try:
            User.objects.get(username=validated_data["username"])
        except ObjectDoesNotExist:
            return User.objects.create_user(**validated_data)

        raise ValidationError({"success": False, "msg": "Username already taken"})
