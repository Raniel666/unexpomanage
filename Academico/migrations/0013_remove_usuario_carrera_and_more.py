# Generated by Django 4.1.5 on 2023-03-10 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0012_alter_registroinscripcion_materias_ids_registropago_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='carrera',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='hora_inscripcion',
        ),
    ]