# Generated by Django 5.0.1 on 2024-03-13 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartscore', '0005_alter_player_end_contract'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shortlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('players', models.ManyToManyField(to='smartscore.player')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='shortlist',
            field=models.ManyToManyField(to='smartscore.shortlist'),
        ),
    ]