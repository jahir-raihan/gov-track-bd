# Generated by Django 4.1.3 on 2022-12-20 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo_app', '0014_proposal_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='recommendation',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]