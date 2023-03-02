# Generated by Django 4.1.6 on 2023-03-01 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0005_alter_registroinscripcion_fecha_inscripcion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroinscripcion',
            name='fecha_inscripcion',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='registroinscripcion',
            name='materias_ids',
            field=models.ManyToManyField(blank=True, null=True, to='Academico.materia'),
        ),
    ]