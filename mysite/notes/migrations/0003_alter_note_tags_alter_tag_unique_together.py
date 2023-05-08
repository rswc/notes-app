# Generated by Django 4.1.7 on 2023-04-06 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_note_color_alter_note_unique_together_tag_note_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(related_name='notes', to='notes.tag'),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together={('user', 'name')},
        ),
    ]