# Generated by Django 4.1.3 on 2022-12-03 05:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='Like', max_length=200)),
                ('summary', models.TextField(blank=True, max_length=256, null=True)),
                ('object', models.CharField(blank=True, max_length=200, null=True)),
                ('postId', models.CharField(blank=True, max_length=200, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authors.single_author')),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('name', models.IntegerField(default=0)),
                ('host', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('api', models.CharField(max_length=255)),
                ('authorization', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('type', models.CharField(default='post', max_length=200)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('id', models.CharField(max_length=200, null=True)),
                ('source', models.CharField(max_length=200, null=True)),
                ('origin', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=256, null=True)),
                ('Categories', models.CharField(default='', max_length=100)),
                ('contentType', models.CharField(choices=[('text/plain', 'Plaintext'), ('text/markdown', 'Markdown'), ('application/base64', 'app'), ('image/png;base64', 'png'), ('image/jpeg;base64', 'jpeg')], default=('text/plain', 'Plaintext'), max_length=30)),
                ('textType', models.CharField(choices=[('text/plain', 'Plaintext'), ('text/markdown', 'Markdown')], default=('text/plain', 'Plaintext'), max_length=30)),
                ('count', models.IntegerField(default=0)),
                ('published', models.DateTimeField(auto_now_add=True, null=True)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('FRIENDS', 'Friends'), ('PRIVATE', 'Specific friend')], default='PUBLIC', max_length=7)),
                ('post_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='authors.single_author')),
            ],
        ),
        migrations.CreateModel(
            name='Liked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='liked', max_length=200)),
                ('postId', models.CharField(blank=True, max_length=200, null=True)),
                ('items', models.ManyToManyField(blank=True, to='post.like')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('id', models.CharField(max_length=200, null=True)),
                ('comment', models.TextField(blank=True, max_length=256, null=True)),
                ('contentType', models.CharField(choices=[('text/plain', 'Plaintext'), ('text/markdown', 'Markdown')], default=('text/plain', 'Plaintext'), max_length=30)),
                ('published', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='authors.single_author')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
    ]
