# Generated by Django 5.1.4 on 2025-01-10 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.TextField()),
            ],
        ),
    ]
