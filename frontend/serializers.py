from rest_framework import serializers
from frontend.models import *

class SystemSerializer(serializers.HyperlinkedModelSerializer):
    # pk = serializers.HyperlinkedRelatedField( view_name='system', read_only=True)
    class Meta:
        model = System
        fields = ('added','name','language','environment','command','pk')

class UploadSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source = 'user.email')
    language = serializers.ChoiceField(choices=sorted([(system.language, system.language) for system in System.objects.all()]))
    systems = serializers.ChoiceField(choices=sorted([(system.name, system.name) for system in System.objects.all()]))
    environment = serializers.ChoiceField(choices=sorted([(system.environment, system.environment) for system in System.objects.all()]))

    
    class Meta:
        model = Upload
        fields = ('pk','user','audiofiles','created','language','systems','metadata','environment')

class FinishedUploadSerializer(UploadSerializer):
    class Meta:
        model = Upload
        fields = ('pk','user','audiofiles','created','language','systems','transcripts','status','metadata','environment')

# class FileListSerializer(serializers.ListSerializer):
#     child = serializers.FileField()
#     def create(self, validated_data):
#         books = [Fiyle(**item) for item in validated_data]
#         return Fiyle.objects.bulk_create(books)

class FileSerializer(serializers.Serializer):
    fiyle = serializers.FileField()

    def create(self, validated_data):
        return Fiyle.objects.create(**validated_data)

    # class Meta:
    #     list_serializer_class = FileListSerializer




class UserSerializer(serializers.HyperlinkedModelSerializer):

    

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'pk')
       

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class AdminUserSerializer(UserSerializer):
    # pk = serializers.HyperlinkedRelatedField( view_name='user', read_only=True)
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','is_staff','is_active','pk','password')

class NewUserSerializer(UserSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name','password')

