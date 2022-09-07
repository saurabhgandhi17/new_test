from rest_framework import serializers
from ..models import PrivateGroupMessagesModel, PrivateMessagesModel, GroupMessagesModel, GroupInfoModel, User


# listout all the users
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# listout all private messages
class PrivateGroupMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateGroupMessagesModel
        exclude = ('content', )

        def create(self, validated_data):
            return PrivateGroupMessagesModel.objects.create(**validated_data)

# listout all private messages
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessagesModel
        fields = ['id', 'content', 'sender', 'receiver', 'group','message_type']


# listout all groups messages
class GroupMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessagesModel
        fields = ['id', 'participants','sender','content','group']


# listout all groups
class GroupSerializer(serializers.ModelSerializer):
    # messages = GroupMessagesSerializer(many=True)
    class Meta:
        model = GroupInfoModel
        # fields = ['id', 'name', 'created_by', 'messages']
        fields = ['id', 'name', 'created_by']
