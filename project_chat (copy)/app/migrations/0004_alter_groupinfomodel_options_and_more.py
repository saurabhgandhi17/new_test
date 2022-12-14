# Generated by Django 4.1 on 2022-09-07 05:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_groupmessagesmodel_is_deleted_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupinfomodel',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'GroupInfoModel'},
        ),
        migrations.AlterModelOptions(
            name='groupmessagesmodel',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'GroupMessagesModel'},
        ),
        migrations.AlterModelOptions(
            name='privatemessagesmodel',
            options={'ordering': ['created_at'], 'verbose_name_plural': 'PrivateMessagesModel'},
        ),
        migrations.AddField(
            model_name='groupinfomodel',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='groupmessagesmodel',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grp_group_name', to='app.groupinfomodel'),
        ),
        migrations.AlterField(
            model_name='groupmessagesmodel',
            name='participants',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grp_participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='privatemessagesmodel',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ono_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='privatemessagesmodel',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ono_senders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='PrivateGroupMessagesModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=1000)),
                ('attachments', models.FileField(blank=True, upload_to='attachments/')),
                ('message_type', models.CharField(choices=[('PRIVATE', 'Private'), ('GROUP', 'Group')], default='Private', max_length=15)),
                ('message_format', models.CharField(choices=[('TEXT', 'Text'), ('AUDIO', 'Audio'), ('VIDEO', 'Video'), ('IMAGE', 'Image')], default='Text', max_length=15)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ono_grp_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ono_grp_sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'PrivateGroupMessagesModel',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='privatemessagesmodel',
            name='group',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='ono_group_name', to='app.privategroupmessagesmodel'),
            preserve_default=False,
        ),
    ]
