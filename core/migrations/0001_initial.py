# Generated by Django 5.0.6 on 2024-05-30 09:01

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
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('code', models.CharField(blank=True, max_length=50)),
                ('picture', models.ImageField(blank=True, default='static/unknown_component.png', upload_to='components_pics')),
                ('datasheet_url', models.URLField(blank=True, max_length=2048)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('row', models.PositiveSmallIntegerField()),
                ('column', models.PositiveSmallIntegerField()),
                ('depth', models.PositiveSmallIntegerField()),
                ('protection', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propic', models.ImageField(blank=True, default='static/unknown_user.png', upload_to='users_pics')),
                ('stars', models.ManyToManyField(blank=True, related_name='stars', to='core.component')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('processed', models.BooleanField(blank=True, default=False)),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.component')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
            options={
                'ordering': ['-date', 'profile'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='requests',
            field=models.ManyToManyField(blank=True, related_name='requests', through='core.Request', to='core.component'),
        ),
        migrations.CreateModel(
            name='Use',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.component')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='uses',
            field=models.ManyToManyField(blank=True, related_name='uses', through='core.Use', to='core.component'),
        ),
    ]
