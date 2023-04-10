# Generated by Django 4.1.5 on 2023-03-06 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upgrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeToUpgrade', models.DateTimeField()),
                ('timeProvisioned', models.DateTimeField()),
                ('user', models.CharField(max_length=100)),
                ('devicesToBeUpgraded', models.ManyToManyField(to='devices.device')),
            ],
        ),
    ]
