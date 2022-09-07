import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CommonFieldModel(models.Model):
    '''
       Model used to store all common fields  
    '''
    MESSAGE_TYPE = (
        ("PRIVATE", "Private"),
        ("GROUP", "Group"),
    )
    MESSAGE_FORMAT = (
        ("TEXT", "Text"),
        ("AUDIO", "Audio"),
        ("VIDEO", "Video"),
        ("IMAGE", "Image"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.CharField(max_length=1000)
    attachments = models.FileField(upload_to='attachments/',blank=True)
    message_type = models.CharField(max_length=15, choices=MESSAGE_TYPE, default='Private')
    message_format = models.CharField(max_length=15, choices=MESSAGE_FORMAT, default='Text')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PrivateGroupMessagesModel(CommonFieldModel):
    '''
        To store the private chat details - entry will ne unique
    '''
    name = models.CharField(max_length=100,unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ono_grp_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ono_grp_receiver")

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "PrivateGroupMessagesModel"

    def __str__(self) -> str:
        return str(self.name)


class PrivateMessagesModel(CommonFieldModel):
    '''
        To store private messages
    '''
    is_seen = models.BooleanField(default=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ono_senders")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ono_receiver")
    group = models.ForeignKey('PrivateGroupMessagesModel',on_delete=models.CASCADE,related_name="ono_group_name")

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "PrivateMessagesModel"

    def __str__(self) -> str:
        return str(self.id)


class GroupInfoModel(models.Model):
    '''
        To store group details
    '''
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="grp_created_by", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "GroupInfoModel"

    def __str__(self) -> str:
        return str(self.id)


class GroupMessagesModel(CommonFieldModel):
    '''
        To store the groups messages, participants etc... 
    '''
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grp_senders")
    participants = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grp_participants")
    group = models.ForeignKey('GroupInfoModel', on_delete=models.CASCADE,related_name="grp_group_name")

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "GroupMessagesModel"

    def __str__(self) -> str:
        return str(self.id)
