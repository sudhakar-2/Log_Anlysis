# Generated by Django 5.0.7 on 2024-07-12 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.TextField()),
                ('Email', models.EmailField(max_length=254)),
                ('Password', models.TextField()),
            ],
        ),
    ]
