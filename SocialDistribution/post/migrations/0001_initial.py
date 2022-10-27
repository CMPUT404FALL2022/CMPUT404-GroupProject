# Generated by Django 3.1.6 on 2022-10-27 07:09

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment', models.TextField(blank=True, null=True)),
                ('published', models.DateTimeField(auto_now_add=True, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('type', models.CharField(default='post', max_length=200)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=256, null=True)),
                ('Categories', models.CharField(default='', max_length=100)),
                ('contentType', models.CharField(choices=[('text/plain', 'Plaintext'), ('text/markdown', 'Markdown'), ('application/base64', 'app'), ('image/png;base64', 'png'), ('image/jpeg;base64', 'jpeg')], default=('text/plain', 'Plaintext'), max_length=30)),
                ('textType', models.CharField(blank=True, choices=[('text/plain', 'Plaintext'), ('text/markdown', 'Markdown')], max_length=30, null=True)),
                ('count', models.IntegerField(default=0)),
                ('published', models.DateTimeField(auto_now_add=True, null=True)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('FRIENDS', 'Friends'), ('PRIVATE', 'Specific friend')], default='PUBLIC', max_length=7)),
            ],
        ),
    ]
