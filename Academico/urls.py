from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

# Acceder a directorio raiz
urlpatterns = [
    path('', views.portada, name="portada"),
    path('pensum/', login_required(views.asignatura_admin), name="pensum"),
    path('cursos/', login_required(views.cursos), name="cursos"),
    path('salir/', login_required(views.salir), name="salir"),
    path('pensum/eliminacionCurso/<codigo>',
         login_required(views.eliminarCurso)),
    path('pensum/edicionCurso/<codigo>',
         login_required(views.edicionCurso), name="editarCurso"),
    path('pensum/editarCurso/', login_required(views.editarCurso), name="editar"),
    path('listarUsuarios/', login_required(views.listadoUsuario.as_view()),
         name="listarUsuarios"),
    path('registrarUsuario/', login_required(views.registrarUsuario.as_view()),
         name="registrarUsuario"),
    path('listarUsuarios/eliminarUsuario/<expediente>',
         login_required(views.eliminarUsuario), name="eliminarUsuario"),
    path('listarUsuarios/edicionUsuario/<expediente>',
         login_required(views.edicionUsuario), name="edicionUsuario"),
    path('listarUsuarios/editarUsuario/',
         login_required(views.editarUsuario), name="editarUsuario"),
    path('inscripciones/', login_required(views.inscripciones), name="inscripciones"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
