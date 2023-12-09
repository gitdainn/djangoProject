# Generated by Django 4.2.7 on 2023-12-03 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='naverDB',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('image', models.URLField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('media_outlet', models.CharField(max_length=255)),
                ('date', models.DateField(blank=True, null=True)),
                ('article_link', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsDB',
            fields=[
                ('id', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('address', models.URLField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('media_outlet', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('category1', models.CharField(max_length=255)),
                ('category2', models.CharField(max_length=255)),
                ('category3', models.CharField(max_length=255)),
                ('entity_location', models.CharField(max_length=255)),
                ('entity_company', models.CharField(max_length=255)),
                ('keywords', models.CharField(max_length=255)),
                ('feature', models.CharField(max_length=255)),
                ('main_body', models.TextField()),
                ('original_source', models.URLField()),
            ],
        ),
    ]