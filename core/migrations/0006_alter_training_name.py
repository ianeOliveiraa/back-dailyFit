# Generated by Django 5.1.3 on 2024-11-23 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_training_exercise_remove_training_repetitions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='name',
            field=models.CharField(db_column='tx_name', max_length=70),
        ),
    ]