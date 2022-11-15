from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role', read_only=True)
    name = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    password_one = serializers.CharField(write_only=True)
    password_two = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['name', 'username', 'role', 'password_one', 'password_two']

    def validate(self, attrs):
        password_one = attrs.get('password_one')
        password_two = attrs.get('password_two')
        if password_two != password_one:
            raise ValidationError({'error': 'The passwords are not equal'})
        validate_password(password=password_two)
        return attrs

    def update(self, instance, validated_data):
        password_two = validated_data.get('password_two')
        instance.set_password(password_two)
        instance.save()
        return instance
