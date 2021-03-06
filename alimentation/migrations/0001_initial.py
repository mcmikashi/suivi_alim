# Generated by Django 3.2 on 2021-05-02 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aliment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=150)),
                ('calorie', models.IntegerField()),
                ('lipides', models.FloatField()),
                ('cholestérol', models.FloatField()),
                ('protéines', models.FloatField()),
                ('potassium', models.FloatField()),
                ('glucides', models.FloatField()),
                ('image', models.FileField(default="pas_d'image_disponible.png", max_length=250, upload_to='aliment/')),
            ],
        ),
    ]
