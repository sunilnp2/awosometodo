# Generated by Django 4.0.5 on 2022-06-23 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todo_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('title', models.TextField()),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
    ]
