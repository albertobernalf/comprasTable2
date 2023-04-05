"""comprasTable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf  import settings
from django.conf.urls.static import  static
from solicitud import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Solicitud

    path('chaining/', include('smart_selects.urls')),
    path('medicalCompras/', views.menuAcceso, name='medical_Compras'),
    path('validaAcceso/', views.validaAcceso),
    path('Solicitudes/<str:username>, <str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>', views.Solicitudes),
    path('guardarSolicitudes/<str:username>, <str:sedeSeleccionada>,<str:nombreUsuario>, <str:fecha>, <str:nombreSede>,<str:perfil>, <str:area>',       views.guardarSolicitudes),

    path('salir/', views.salir),
    path('solicitudesConsultaTrae/<str:username>, <str:sedeSeleccionada>,<str:nombreUsuario>, <str:nombreSede>,<str:perfil>/', views.PostStoreSolicitudesConsulta.as_view(), name='post_storeSolicitudesConsulta'),
    path('solicitudesConsultaTrae', views.PostStoreSolicitudesConsulta.as_view(), name='post_storeSolicitudesConsulta'),
    path('solicitudesConsulta/<str:username>, <str:sedeSeleccionada>,<str:nombreUsuario>, <str:nombreSede>,<str:perfil>/', views.SolicitudesConsulta, name='SolicitudesConsulta'),
    path('load_dataSolicitudesConsulta/<str:data>/', views.load_dataSolicitudesConsulta, name='load_dataSolicitudesConsulta'),

    # Validacion

    path('ValidacionConsulta/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>', views.PostStoreValidacion.as_view(),name='post_storeValidacion'),
    path('ValidacionConsulta/ValidacionBusca/<str:solicitudId>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>/', views.PostStoreValidacion.as_view(),name='post_storeValidacion'),
    path('ValidacionConsulta/ValidacionBusca/', views.PostStoreValidacion.as_view(),name='post_storeValidacion'),
    path('Validacion/post_editValidacion/<int:id>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>,<str:solicitudId>/edit/', views.post_editValidacion, name='post_editValidacion'),
    path('load_dataValidacion/<str:data>', views.load_dataValidacion, name='load_dataValidacion'),

    # Fin Validacion

    # Almacen
    path('AlmacenConsulta/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>', views.PostStoreAlmacen.as_view(), name='post_storeAlmacen'),
    path('AlmacenConsulta/', views.PostStoreAlmacen.as_view(), name='post_storeAlmacen'),

    path('load_dataAlmacen/<str:data>', views.load_dataAlmacen, name='load_dataAlmacen'),
    path('AlmacenConsulta/postAlmacen/<int:id>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>,<str:solicitudId>/edit/', views.post_editAlmacen, name='post_editAlmacen'),
    path('postAlmacen/<int:id>/delete', views.post_deleteAlmacen, name='post_deleteAlmacen'),
    path('AlmacenConsulta/AlmacenBusca/postAlmacen/<int:id>/delete', views.post_deleteAlmacen, name='post_deleteAlmacen'),

    # Fin Almacen

    # Compras

    #path('ComprasConsulta/<str:username>, <str:sedeSeleccionada>,<str:nombreUsuario>, <str:nombreSede>,<str:perfil>',  views.ComprasConsulta),
    path('ComprasConsulta/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>',  views.PostStoreCompras.as_view() , name='post_storeCompras'),
    path('ComprasConsulta/ComprasBusca', views.PostStoreCompras.as_view(), name='post_storeCompras'),

    path('fetch/>', views.load_dataCompras, name='load_dataCompras'),
    path('load_dataCompras/<str:data>', views.load_dataCompras, name='load_dataCompras'),
    path('ComprasConsulta/postCompras/<int:id>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>,<str:solicitudId>/edit/', views.post_editCompras, name='post_editCompras'),
    #path('postCompras/<int:id>/delete', views.post_deleteCompras, name='post_deleteCompras'),
    #path('ComprasConsulta/ComprasBusca/postCompras/<int:id>/delete', views.post_deleteCompras, name='post_deleteCompras'),

    # Fin Compras

    # Ordenes de Compras
    path('ordenesCompra/<str:username>, <str:sedeSeleccionada>,<str:nombreUsuario>, <str:nombreSede>,<str:perfil>', views.OrdenesCompraConsulta1, name='Compras_Consulta'),
    path('ordenesCompra/OrdenesCompraBusca/', views.PostStoreOrdenesCompra.as_view(),name='post_storeOrdenesCompra' ),
    path('ordenesCompra/OrdenesCompraBusca/<str:pk>,<str:btnEnviarSol>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>/', views.PostStoreOrdenesCompra.as_view(),name='post_storeOrdenesCompra'),
    path('/ordenesCompra/OrdenesCompraBusca/<str:pk>,<str:btnEnviarSol>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:perfil>/', views.PostStoreOrdenesCompra.as_view(),name='post_storeOrdenesCompra'),
    path('load_dataOrdenesCompra/<str:solicitudId>', views.load_dataOrdenesCompra, name='load_dataOrdenesCompra'),
    path('descargaArchivo/<str:archivo>', views.descargaArchivo),


    path('ordenesCompraConsultaTrae/<str:username>, <str:sedeSeleccionada>,<str:nombreUsuario>, <str:nombreSede>,<str:perfil>/', views.PostStoreOrdenesCompraConsulta.as_view(), name='post_storeOrdenesCompraConsulta'),
    path('ordenesCompraConsultaTrae', views.PostStoreOrdenesCompraConsulta.as_view(), name='post_storeOrdenesCompraConsulta'),
    path('ordenesCompraConsulta/<str:username>, <str:sedeSeleccionada>,<str:nombreUsuario>, <str:nombreSede>,<str:perfil>/', views.OrdenesCompraConsulta, name='OrdenesCompraConsulta'),
    path('load_dataOrdenesCompraConsulta/<str:data>/', views.load_dataOrdenesCompraConsulta, name='load_dataOrdenesCompraConsulta'),

    # Fin Ordenes de Compras

    ## Pruebas carga Files


    path('ComprasConsulta/descargaArchivoAjax/<int:pk>', views.Simple_Upload, name='post_descargaArchivo'),
    path('ComprasConsulta/descargaArchivoAjax', views.Simple_Upload, name='post_descargaArchivo'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Añadir
admin.site.site_header = 'Administracion Medical Compras'
admin.site.site_title = "Portal de Medical Compras"
admin.site.index_title = "Bienvenidos al portal de administración Medical Compras"


