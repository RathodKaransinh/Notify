# Generated by Django 5.0.3 on 2024-03-17 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_notice_keywords'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NoticeKeywords',
            new_name='NoticeKeyword',
        ),
    ]
