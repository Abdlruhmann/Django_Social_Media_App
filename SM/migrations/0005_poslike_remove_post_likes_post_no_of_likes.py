# Generated by Django 5.0.6 on 2024-06-03 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SM', '0004_post_likes_alter_profile_profile_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.AddField(
            model_name='post',
            name='no_of_likes',
            field=models.IntegerField(default=0, verbose_name='no_of_likes'),
        ),
    ]
