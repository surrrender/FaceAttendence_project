# Generated by Django 5.1.4 on 2024-12-24 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FA', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbsentPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]