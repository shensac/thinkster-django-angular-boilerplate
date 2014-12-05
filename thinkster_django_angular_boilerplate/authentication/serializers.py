from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from thinkster_django_angular_boilerplate.authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('email', 'username',
                  'first_name', 'last_name', 'tagline', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

    def update(self, instance, validated_data):
        print 'outside'
        if instance is not None:
            print 'inside'
            instance.username = validated_data.get('username',
                                                   instance.username)
            instance.tagline = validated_data.get('tagline', instance.tagline)

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

                update_session_auth_hash(self.context.get('request'), instance)

        return instance

    def create(self, validated_data):
        print 'in serz create'
        return Account(**validated_data)
