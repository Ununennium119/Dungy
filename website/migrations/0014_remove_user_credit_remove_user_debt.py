# Generated by Django 4.2 on 2023-06-04 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_costmember_remove_cost_members_alter_user_friends_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='credit',
        ),
        migrations.RemoveField(
            model_name='user',
            name='debt',
        ),
    ]
