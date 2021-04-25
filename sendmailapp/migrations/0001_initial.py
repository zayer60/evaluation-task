# Generated by Django 3.2 on 2021-04-25 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE')], default='male', max_length=100)),
                ('dob', models.DateField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='PatientGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sendmailapp.group')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sendmailapp.patient')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='groups',
            field=models.ManyToManyField(blank=True, through='sendmailapp.PatientGroup', to='sendmailapp.Group'),
        ),
    ]
