# Generated by Django 5.1.2 on 2024-10-28 20:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, help_text='Enter the category name.', max_length=100, unique=True, verbose_name='Category Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the post title.', max_length=100, verbose_name='Post Title')),
                ('content', models.TextField(blank=True, help_text='Enter the post content.', null=True, verbose_name='Post Content')),
                ('image', models.ImageField(blank=True, help_text='Upload the post image.', null=True, upload_to='posts/', verbose_name='Post Image')),
                ('published_at', models.DateField(help_text='Enter the published date of the post.', verbose_name='Published At')),
                ('author', models.ForeignKey(help_text='Select the author of the post.', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('categories', models.ManyToManyField(blank=True, help_text='Select the categories of the post.', related_name='posts', to='blog.category', verbose_name='Categories')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(help_text='Enter the comment content.', verbose_name='Comment Content')),
                ('post', models.ForeignKey(help_text='Select the post of the comment.', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post', verbose_name='Post')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
