from datetime import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.views.generic import CreateView, ListView
from .forms import AsignaturaForm, FormularioUsuario
from .models import Materia, Usuario, Departamento, Carrera, RegistroInscripcion
from django.contrib import messages
from .carrito import Carrito



def portada(request):

    return render(request, "portada.html")

# Create your views here.


def asignatura_admin(request):
    form = AsignaturaForm()
    # En una variable guardamos todos los materia de una db
    asignaturas = Materia.objects.all()
    print(asignaturas)
    if request.method == 'POST':
        form = AsignaturaForm(data=request.POST)
        try:
            if form.is_valid():
                form.save()
                # Datos correctos
                messages.success(request, "Curso Registrado!")
                return redirect('academico:pensum')
        except ValueError:
            return render(request, '/pensum', {"asignaturas": asignaturas, "form": form, 'error': 'Ingresa valores correctamente'})

    messages.success(request, "Cursos listados!")

    return render(request, "materia.html", {"asignaturas": asignaturas, "form": form})


def eliminarCurso(request, codigo):
    asignatura = Materia.objects.get(codigo=codigo)
    asignatura.delete()

    messages.success(request, "Curso Eliminado!")

    return redirect("academico:pensum")


def edicionCurso(request, codigo):
    asignatura = Materia.objects.get(codigo=codigo)
    return render(request, "edicion_materia.html", {"asignatura": asignatura})


def editarCurso(request):
    codigo = request.POST['codigo']
    nombre = request.POST['nombre']
    unidades = request.POST['num_unidades']
    credito_requerido = request.POST['credito_requerido']
    cantidadmax_estudiantes = request.POST['cantidadmax_estudiantes']
    cantidad_estudiantes = request.POST['cantidad_estudiantes']
    carrera = request.POST['carrera']

    abierta = request.POST.get('abierta', False)
    abierta_bool = False
    if abierta == 'on':
        abierta_bool = True

    asignatura = Materia.objects.get(codigo=codigo)
    asignatura.nombre = nombre
    asignatura.unidades = unidades
    asignatura.credito_requerido = credito_requerido
    asignatura.cantidadmax_estudiantes = cantidadmax_estudiantes
    asignatura.cantidad_estudiantes = cantidad_estudiantes
    asignatura.abierta = abierta_bool
    asignatura.carrera = carrera
    asignatura.save()

    messages.success(request, "Curso Actualizado!")

    return redirect("academico:pensum")


def cursos(request):
    carreras = Carrera.objects.all()
    return render(request, "index.html", {"carreras": carreras})


def seleccion_carrera(request, codigo):
    # Obtengo la tabla de las carreras
    carrera = Carrera.objects.get(codigo_c=codigo)
    # Obtengo los semestres de la clase Materia
    semestres = Materia().opciones_semestres
    semestre_dict = {}
    if carrera:
        # Si existe la carrera traeme los departamentos de esa carrera
        departamentos = Departamento.objects.filter(carrera_ids=codigo)
        # Guarda en un diccionario las materias por semestre
        for semestre in semestres:
            semestre_dict[f"{semestre[1]}"] = []
            for departamento in departamentos:
                dpto_code = departamento.codigo_dep
                materias = Materia.objects.filter(departamento_id=dpto_code, semestre=semestre[0])
                for materia in materias:
                    semestre_dict[f"{semestre[1]}"].append(materia)

        return render(request, "prueba.html", {"carrera": carrera, "materias_semestre": semestre_dict})


def salir(request):
    logout(request)
    return redirect('/')


class listadoUsuario(ListView):
    model = Usuario
    template_name = 'listar_usuario.html'

    def get_queryset(self):
        return self.model.objects.filter(usuario_activo=True)


class registrarUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = 'crear_usuario.html'
    success_url = reverse_lazy('academico:listarUsuarios')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nuevo_usuario = Usuario(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                nombres=form.cleaned_data['nombres'],
                apellidos=form.cleaned_data['apellidos'],
                expediente=form.cleaned_data['expediente'],
                cedula=form.cleaned_data['cedula'],
                creditos_aprobados=form.cleaned_data['creditos_aprobados'],
                carrera=form.cleaned_data['carrera'],
                semestre=form.cleaned_data['semestre'],
                tipo_estudiante=form.cleaned_data['tipo_estudiante'],
                imagen=form.cleaned_data['imagen'],
                fecha_inscripcion=form.cleaned_data['fecha_inscripcion'],
                hora_inscripcion=form.cleaned_data['hora_inscripcion'],
            )
            nuevo_usuario.set_password(form.cleaned_data['password1'])
            nuevo_usuario.save()
            return redirect('academico:listarUsuarios')
        else:
            return render(request, self.template_name, {'form': form})


def eliminarUsuario(request, expediente):
    user = Usuario.objects.get(expediente=expediente)
    user.delete()

    return redirect("academico:listarUsuarios")


def edicionUsuario(request, expediente):
    user = Usuario.objects.get(expediente=expediente)
    return render(request,  "edicion_usuario.html", {"user": user})


def editarUsuario(request):
    expediente = request.POST['expediente']
    nombres = request.POST['nombres']
    apellidos = request.POST['apellidos']
    username = request.POST['username']
    email = request.POST['email']
    cedula = request.POST['cedula']
    creditos_aprobados = request.POST['creditos_aprobados']
    carrera = request.POST['carrera']
    semestre = request.POST['semestre']
    tipo_estudiante = request.POST['tipo_estudiante']
    fecha_inscripcion = request.POST['fecha_inscripcion']
    hora_inscripcion = request.POST['hora_inscripcion']

    user = Usuario.objects.get(expediente=expediente)
    user.nombres = nombres
    user.apellidos = apellidos
    user.username = username
    user.email = email
    user.cedula = cedula
    user.creditos_aprobados = creditos_aprobados
    user.carrera = carrera
    user.semestre = semestre
    user.tipo_estudiante = tipo_estudiante
    user.fecha_inscripcion = fecha_inscripcion
    user.hora_inscripcion = hora_inscripcion
    user.save()

    return redirect("academico:listarUsuarios")


def inscripciones(request):
    # Obtengo la tabla de las carreras
    codigo = request.user.carrera_id.codigo_c
    estudiante = request.user.id
    carrera = Carrera.objects.get(codigo_c=codigo)
    # Obtengo los registros de inscripcion del estudiantye
    registros_ins = RegistroInscripcion.objects.filter(estudiante_id=estudiante)
    for registro in registros_ins:
        estado = registro.estado
    # Obtengo los semestres de la clase Materia
    semestres = Materia().opciones_semestres
    semestre_dict = {}
    if carrera:
        # Si existe la carrera traeme los departamentos de esa carrera
        departamentos = Departamento.objects.filter(carrera_ids=codigo)
        # Guarda en un diccionario las materias por semestre
        for semestre in semestres:
            semestre_dict[f"{semestre[1]}"] = []
            for departamento in departamentos:
                dpto_code = departamento.codigo_dep
                materias = Materia.objects.filter(departamento_id=dpto_code, semestre=semestre[0])
                for materia in materias:
                    semestre_dict[f"{semestre[1]}"].append(materia)

        return render(request, "inscripciones.html", {"carrera": carrera, "materias_semestre": semestre_dict, "inscripcion_estado": estado})

    # asignaturas = Materia.objects.all()
    # return render(request, "inscripciones.html", {"asignaturas": asignaturas})


def agregar_materia(request, codigo):
    carrito = Carrito(request)
    asignatura = Materia.objects.get(codigo=codigo)
    carrito.agregar(asignatura)
    return redirect("academico:inscripciones")


def eliminar_materia(request, codigo):
    carrito = Carrito(request)
    asignatura = Materia.objects.get(codigo=codigo)
    carrito.eliminar(asignatura)
    return redirect("academico:inscripciones")


def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return redirect("academico:inscripciones")


# Accion para guardar los datos en la tabla de inscripciones
def registrar_inscripcion(request):
    carrito = Carrito(request).carrito
    estudiante_id = request.user.id
    registros_inscripcion = RegistroInscripcion.objects.filter(estudiante_id=estudiante_id, estado="pagado")

    if registros_inscripcion:
        for registro in registros_inscripcion:
            materias = registro.materias_ids.all()

        context = {"registros_inscripcion": registros_inscripcion, "materias": materias}
        return render(request, "pago_views.html", context)

    else:
        registros_inscripcion = RegistroInscripcion.objects.filter(estudiante_id=estudiante_id, estado="pendiente")
        if registros_inscripcion:
            for registro in registros_inscripcion:
                materias_ids = [materia_id for materia_id in carrito.keys()]
                materias = Materia.objects.filter(codigo__in=materias_ids)
                registro.materias_ids.set(materias)
                registro.estado = "pagado"
                registro.fecha_inscripcion = datetime.now()
                registro.save()

                materias = registro.materias_ids.all()

            context = {"registros_inscripcion": registros_inscripcion, "materias": materias}
            return render(request, "pago_views.html", context)
        else:
            context = {"registros_inscripcion": [], "materias": []}
            return render(request, "pago_views.html", context)


def volver_pendiente(request):
    estudiante_id = request.user.id
    registros_inscripcion = RegistroInscripcion.objects.filter(estudiante_id=estudiante_id, estado="pagado")

    if registros_inscripcion:
        for registro in registros_inscripcion:
            registro.estado = "pendiente"
            registro.save()

    return redirect("academico:inscripciones")
