# Generated by Django 5.1 on 2024-09-01 10:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_user_alter_postrecipient_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='postrecipient',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
