# Generated by Django 4.0.5 on 2023-03-16 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_admins_requests', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_rooms_requests', to='app.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_users_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'room', 'admin')},
            },
        ),
    ]