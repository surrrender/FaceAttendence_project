# Generated by Django 5.1.4 on 2024-12-25 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FA', '0002_classinstance_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classinstance',
            name='face_encoding',
        ),
        migrations.AddField(
            model_name='absentperson',
            name='class_instance',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='FA.classinstance'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classinstance',
            name='lecture',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='faceencoding',
            name='class_instance',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='FA.classinstance'),
            preserve_default=False,
        ),
    ]
