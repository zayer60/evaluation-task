# Generated by Django 3.2 on 2021-04-25 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendmailapp', '0002_alter_patient_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='groups',
            field=models.ManyToManyField(blank=True, through='sendmailapp.PatientGroup', to='sendmailapp.Group'),
        ),
    ]
