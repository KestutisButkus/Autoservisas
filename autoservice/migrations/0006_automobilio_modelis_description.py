# Generated by Django 5.1.3 on 2024-12-05 13:58

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0005_uzsakymas_terminas_alter_uzsakymas_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='automobilio_modelis',
            name='description',
            field=tinymce.models.HTMLField(default='aprašymas'),
            preserve_default=False,
        ),
    ]
