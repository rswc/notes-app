# Generated by Django 4.1.7 on 2023-05-10 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_alter_note_tags_alter_tag_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='cover',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='note',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='note',
            name='color',
            field=models.CharField(choices=[('W', 'White'), ('Y', 'Yellow'), ('G', 'Green'), ('P', 'Pink')], default='W', max_length=1),
        ),
        migrations.AlterField(
            model_name='note',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]