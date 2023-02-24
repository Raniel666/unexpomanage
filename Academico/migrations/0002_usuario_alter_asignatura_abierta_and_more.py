# Generated by Django 4.1.3 on 2023-02-24 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Academico', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='Nombre de usuario')),
                ('expediente', models.CharField(max_length=10, unique=True, verbose_name='Expediente')),
                ('cedula', models.CharField(blank=True, max_length=8, null=True, unique=True, verbose_name='Cedula')),
                ('creditos_aprobados', models.IntegerField(blank=True, null=True, verbose_name='Creditos Aprobados')),
                ('fecha_inscripcion', models.DateField(blank=True, null=True, verbose_name='Fecha de inscripcion')),
                ('hora_inscripcion', models.TimeField(blank=True, null=True, verbose_name='Hora de inscripcion')),
                ('carrera', models.CharField(blank=True, choices=[('Industrial', 'Ingieneria Industrial'), ('Mecanica', 'Ingieneria Mecanica'), ('Sistemas', 'Ingieneria Sistemas')], max_length=15, null=True, verbose_name='Carrera')),
                ('tipo_estudiante', models.CharField(blank=True, choices=[('C', 'Completo'), ('P', 'Parcial')], max_length=15, null=True, verbose_name='Tipo de estudiante')),
                ('semestre', models.IntegerField(blank=True, choices=[(1, 'Semestre 1'), (2, 'Semestre 2'), (3, 'Semestre 3'), (4, 'Semestre 4'), (5, 'Semestre 5'), (6, 'Semestre 6'), (7, 'Semestre 7'), (8, 'Semestre 8'), (9, 'Semestre 9'), (10, 'Semestre 10')], null=True)),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Correo electronico')),
                ('nombres', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombres')),
                ('apellidos', models.CharField(blank=True, max_length=100, null=True, verbose_name='apellidos')),
                ('imagen', models.ImageField(blank=True, max_length=200, null=True, upload_to='perfil/', verbose_name='Imagen de perfil')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='asignatura',
            name='abierta',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='asignatura',
            name='codigo',
            field=models.CharField(max_length=5, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'pedido',
                'verbose_name_plural': 'pedidos',
                'db_table': 'pedidos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LineaPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('codigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Academico.asignatura')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'lineapedido',
                'verbose_name_plural': 'lineapedidos',
                'db_table': 'lineapedidos',
                'ordering': ['id'],
            },
        ),
    ]
