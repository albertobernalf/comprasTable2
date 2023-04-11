from django.shortcuts import render



# Create your views here.
from django.shortcuts import render
import re
from django.http import FileResponse
import psycopg2
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
import json
from django.views.generic import ListView, CreateView, TemplateView
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models.functions import Cast, Coalesce
import numpy  as np
from django.utils.encoding import smart_str
from datetime import datetime
from django.urls import reverse, reverse_lazy
import numpy as np
import time
import _thread

import pylab as pl
from unicodedata import normalize


## De Reporteador

import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from django.core import serializers
from io import StringIO
from io import BytesIO
import itertools


#from datascience import *

from django.conf import settings
import os
from datetime import datetime
from datetime import date

from email.message import EmailMessage
import smtplib
from email import encoders

import json
from .forms import solicitudesDetalleForm, solicitudesForm, ordenesCompraForm
from solicitud.models import Solicitudes, SolicitudesDetalle, EstadosValidacion, OrdenesCompra
from django.views.generic import View
from django.views.generic import TemplateView , CreateView

import openpyxl
from openpyxl.styles import Font
from decimal import Decimal

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

from django.http.response import HttpResponse
import mimetypes
import os


# Create your views here.

def index(request):
    print ("Entre index")

    return render(request, 'index.html')


def menuAcceso(request):
    print ("Ingreso al Menu Compras")
    context = {}

    # Sedes
    miConexion  = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432" , user="postgres", password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = 'SELECT ltrim(codreg_sede), nom_sede FROM public.solicitud_sedesCompra'
    cur.execute(comando)
    print(comando)

    sedes = []

    for codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'codreg_sede':codreg_sede, 'nom_sede' : nom_sede})
    miConexion.close()

    context['Sedes'] = sedes

    return render(request, "accesoPrincipal.html", context)


def validaAcceso(request):

    print ("Entre Validacion Acceso Compras")
    context = {}

    # Sedes
    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = 'SELECT id, codreg_sede, nom_sede FROM public.solicitud_sedesCompra'
    cur.execute(comando)
    print(comando)

    sedes = []

    for id,codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'id' : id, 'codreg_sede': codreg_sede, 'nom_sede': nom_sede})
    miConexion.close()

    context['Sedes'] = sedes
    print ("Aqui estan las sedes")
    print (context['Sedes'])

    username = request.POST["username"]
    contrasena = request.POST["password"]
    sedeSeleccionada   = request.POST["seleccion2"]
    print ("sedeSeleccionada = " , sedeSeleccionada)
    print("username = ", username)
    print ("contrasena = ", contrasena)
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada


    # Consigo Nombre de la sede

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                              password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = "SELECT id,codreg_sede, nom_sede FROM public.solicitud_sedesCompra WHERE codreg_sede = '" + sedeSeleccionada + "'"
    #comando = 'SELECT codreg_sede, nom_sede FROM public."Administracion_imhotep_sedesreportes" where estadoReg=' + "'A'"
    cur.execute(comando)
    print(comando)

    nombreSede = []

    for id,codreg_sede, nom_sede in cur.fetchall():
        nombreSede.append({'id' : id,'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

    miConexion.close()

    context['NombreSede'] = nombreSede[0]['nom_sede']

    # Validacion Usuario existente

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = "SELECT num_identificacion, nom_usuario, clave_usuario, carg_usuario, sede_id, perfil  FROM public.solicitud_usuarios WHERE estadoReg = '" + "A' and num_identificacion = '" + username + "'"
    cur.execute(comando)
    print(comando)

    nombreUsuario = []

    for num_identificacion, nom_usuario, clave_usuario , carg_usuario,sede_id , perfil in cur.fetchall():
        nombreUsuario.append({'num_identificacion': num_identificacion, 'nom_usuario': nom_usuario, 'clave_usuario' : clave_usuario, 'carg_usuario':carg_usuario,'sede_id':sede_id, 'perfil':perfil})

    print ("PASE 0")

    context['NombreUsuario'] = nombreUsuario[0]['nom_usuario']
    print ("PASE 1")

    print ("Asi quedo el nombre del usuario",  context['NombreUsuario'])
    miConexion.close()

    perfil =  nombreUsuario[0]['perfil']

    context['Perfil'] = perfil

    if nombreUsuario == []:

        context['Error'] = "Personal invalido y/o No Activo ! "
        print("Entre por personal No encontrado")

        return render(request, "accesoPrincipal.html", context)

        print("pase0")

    else:
        # Valido contraseña
        if nombreUsuario[0]['clave_usuario'] != contrasena:
            context['Error'] = "Contraseña invalida ! "
            return render(request, "accesoPrincipal.html", context)

        else:
            pass

            # Valido la Sede seleccinada

            miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                          password="BD_m3d1c4l")
            cur = miConexion.cursor()

            #comando = "SELECT num_identificacion  FROM public.solicitud_usuarios WHERE estadoReg='A' and num_identificacion = '" + username + "' and codreg_sede =  '"  + sedeSeleccionada + "'"
            comando = "SELECT num_identificacion,nom_sede  FROM public.solicitud_usuarios usu, public.solicitud_sedesCompra sedes WHERE usu.sede_id = sedes.id and usu.estadoReg='A' and usu.num_identificacion = '" + username + "' and sedes.codreg_sede =  '" + sedeSeleccionada + "'"
            print(comando)
            cur.execute(comando)

            permitido = []

            for num_identificacion, nom_sede in cur.fetchall():
                permitido.append({'num_identificacion': num_identificacion, 'nom_sede': nom_sede})

            miConexion.close()


            if permitido == []:

                context['Error'] = "Usuario no tiene autorizacion para la sede seleccionada y/o Reportes no asignados ! "
                return render(request, "accesoPrincipal.html", context)

            else:
                pass
                print("Paso Autenticacion")

    xx=nombreUsuario[0]['nom_usuario']
    yy=nombreSede[0]['nom_sede']

    print("Asi quedo el nombre del usuario", context['NombreUsuario'])
    #return render(request, "Reportes/cabeza.html", context)
    ## el render aquip /solicitudesConsultaTrae/{{Username}}, {{SedeSeleccionada}}, {{NombreUsuario}} , {{NombreSede}}, {{Perfil}}
    #return HttpResponseRedirect(reverse('post_storeSolicitudesConsulta'), {'Username':username, 'SedeSeleccionada':sedeSeleccionada, 'NombreUsuario':xx, 'NombreSede':yy, 'Perfil':perfil})
    #return redirect(reverse('post_storeSolicitudesConsulta', kwargs={'Username':username, 'SedeSeleccionada':sedeSeleccionada, 'NombreUsuario':xx, 'NombreSede':yy, 'Perfil':perfil}))
    return render(request, "Reportes/cabeza.html", context)



def salir(request):
    print("Voy a salir Compras")

    context = {}
    # Sedes
    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()

    comando = 'SELECT codreg_sede, nom_sede FROM public.solicitud_sedesCompra'
    cur.execute(comando)
    print(comando)

    sedes = []

    for codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})
    miConexion.close()

    context['Sedes'] = sedes
    print("Aqui estan las sedes")
    print(context['Sedes'])

    return render(request, "accesoPrincipal.html", context)


def Solicitudes(request , username, sedeSeleccionada, nombreUsuario, nombreSede, perfil):
    pass
    print ("Entre crear solicitudes");
    context = {}
    print("username = ", username)
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    #context['solicitudesForm'] = solicitudesForm
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil

    print("SedeSeleccionada = ", sedeSeleccionada)


    # Combo descripcionescompra

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    cur = miConexion.cursor()

    comando = "SELECT t.id id, t.nombre  nombre FROM public.solicitud_descripcioncompra t where estadoReg='A'"
    cur.execute(comando)
    print(comando)

    descripcionescompra = []
    descripcionescompra.append({'id': '', 'nombre': ''})

    for id, nombre in cur.fetchall():
        descripcionescompra.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(descripcionescompra)

    context['Descripcionescompra'] = descripcionescompra

    # Fin combo descripcionescompra

    # Combo solicitud_tiposcompra

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    cur = miConexion.cursor()

    comando = "SELECT t.id id, t.nombre  nombre FROM public.solicitud_tiposcompra t where estadoReg='A'"
    cur.execute(comando)
    print(comando)

    tiposCompra = []
    tiposCompra.append({'id': '', 'nombre': ''})

    for id, nombre in cur.fetchall():
        tiposCompra.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(tiposCompra)

    context['TiposCompra'] = tiposCompra

    # Fin combo solicitud_presentacion

    # Combo solicitud_tiposcompra

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()

    comando = "SELECT t.id id, t.nombre  nombre FROM public.solicitud_presentacion t where estadoReg='A'"
    cur.execute(comando)
    print(comando)

    presentacion = []
    presentacion.append({'id': '', 'nombre': ''})

    for id, nombre in cur.fetchall():
        presentacion.append({'id': id, 'nombre': nombre})

    miConexion.close()
    print(presentacion)

    context['Presentacion'] = presentacion

    # Fin combo solicitud_presentacion

    # Combo productos


    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")

    comando = 'SELECT t."codregArticulo" codreg_articulo,  t.articulo  articulo   FROM public.solicitud_articulos t order by t.articulo'
    cur.execute(comando)
    print(comando)

    articulos = []
    articulos.append({'id': '', 'nombre': ''})

    for codreg_articulo, articulo in cur.fetchall():
        articulos.append({'codreg_articulo': codreg_articulo, 'articulo': articulo})

    miConexion.close()
    print(articulos)

    context['Articulos'] = articulos

    # Combo Areas

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")
    comando = "SELECT areas.id id ,areas.area  area FROM public.solicitud_areas areas, public.solicitud_sedesCompra sedes WHERE areas.estadoreg = 'A' and areas.sede_id = sedes.id and  sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"

    cur.execute(comando)
    print(comando)

    areas = []
    areas.append({'id': '', 'area': ''})

    for id, area in cur.fetchall():
        areas.append({'id': id, 'area': area})

    miConexion.close()

    context['Areas'] = areas
    print("Estas son las Areas = " , areas)

    # Fin Combo Areas


    print("Estas son las areas = " , context['Areas'])

    # Fin combo Productos

    print ("perfil = ", perfil)

    return render(request, "Reportes/Solicitudes.html", context)


def guardarSolicitudes(request, username,sedeSeleccionada,nombreUsuario,fecha,nombreSede,perfil,area):
    pass
    if request.method == 'POST':
        if request.is_ajax and request.method == "POST":
            print("Entre Ajax")
            username = request.POST["username"]
            nombreSede = request.POST["nombreSede"]
            nombreUsuario = request.POST["nombreUsuario"]
            fecha = request.POST["fecha"]
            area = request.POST["area"]
            estadoReg='A'


            print ("Entre solicitudes Respuesta")
            print(username)
            print (nombreSede)
            print(nombreUsuario)
            print(fecha)
            print(area)

            if (area==""):
                return HttpResponse('Favor ingresar el Area de envio . ' )

            # Consigo el id del usuario :

            miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                          password="BD_m3d1c4l")
            cur = miConexion.cursor()
            comando = "SELECT id,num_identificacion, nom_usuario FROM public.solicitud_usuarios WHERE estadoReg = '" + "A' and num_identificacion = '" + username + "'"
            cur.execute(comando)
            print(comando)

            Usuario = []

            for id, num_identificacion, nom_usuario in cur.fetchall():
                Usuario.append(
                    {'id': id, 'num_identificacion': num_identificacion, 'nom_usuario': nom_usuario})

            miConexion.close()

            usuarioId = Usuario[0]['id']
            print(usuarioId)

            miConexiont = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                          password="BD_m3d1c4l")
            curt = miConexiont.cursor()

            comando = "INSERT INTO solicitud_solicitudes (fecha , estadoReg , area_id, usuarios_id) VALUES ('" + str(
                fecha) + "', '" + str(estadoReg) + "',  '" + str(area) + "', '" + str(
                usuarioId)  + "') RETURNING id;"

            print(comando)
            resultado = curt.execute(comando)
            print("resultado =", resultado)
            n = curt.rowcount
            print("Registros commit = ", n)

            miConexiont.commit()
            solicitudId = curt.fetchone()[0]

            print("solicitudId = ", solicitudId)
            miConexiont.close()

            print("El id de solicitud es  ", solicitudId)

            # Fin grabacion Solictud de Compra


            # Grabacion Solicitud
            print ("Entre a ver detalle solicitud")
            Envio = request.POST["jsonDefSol1"]

            print ("Envio1 = ", Envio)

            JsonDicEnvio = json.loads(Envio)
            print("Diccionario Envio1 = ", JsonDicEnvio)



            # Voy a iterar
            campo = {}
            item = 1

            for x in range(0, len(JsonDicEnvio)):
                print(JsonDicEnvio[x])
                campo1 = JsonDicEnvio[x]
                campo = json.loads(campo1)
                print(campo['descripcion'])
                print(campo['tipo'])
                print(campo['producto'])
                print(campo['presentacion'])
                print(campo['cantidad'])
                print(campo['justificacion'])
                descripcion =  campo['descripcion']
                tipo = campo['tipo']
                producto = campo['producto']
                presentacion = campo['presentacion']
                cantidad = campo['cantidad']
                justificacion = campo['justificacion']
                producto = campo['producto']


                # Aqui obligo a ingresar informacion:

                # Aqui busco los id de cada cosa

                # Consigo Id username

                miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                              password="BD_m3d1c4l")
                cur = miConexion.cursor()
                comando = "SELECT id FROM public.solicitud_usuarios WHERE num_identificacion  = '" + username + "'"
                cur.execute(comando)
                print(comando)

                #usernameId = []
                usernameId = []

                for id in cur.fetchall():
                 usernameId.append({'id':id})
                   #usernameId['id'] = id

                miConexion.close()

                print ("V A L O R E S ")
                print (usernameId)
                print(usernameId[0])
                print(usernameId[0]['id'])
                #print(usernameId['id'])

                print("dato")
                for dato in usernameId:
                    print(dato)
                    print (dato['id'])
                    print(json.dumps(dato['id']))
                    usuario1 = json.dumps(dato['id'])

                print("usuario1 = ", usuario1)
                usuario1 = usuario1.replace('[','')
                usuario1 = usuario1.replace(']', '')
                print("usuario1 = ", usuario1)


                # Fin  Consigo Id username

                # Consigo Id descripcion

                miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                              password="BD_m3d1c4l")
                cur = miConexion.cursor()
                comando = "SELECT id FROM public.solicitud_descripcioncompra WHERE nombre  = '" + descripcion + "'"
                cur.execute(comando)
                print(comando)

                descripcionId = []

                for id in cur.fetchall():
                    descripcionId.append({'id': id})

                miConexion.close()

                print("dato")
                for dato in descripcionId:
                    print(dato)
                    print(dato['id'])
                    print(json.dumps(dato['id']))
                    descripcion1 = json.dumps(dato['id'])

                print("descripcionId = ", descripcionId)
                descripcion1 = descripcion1.replace('[', '')
                descripcion1 = descripcion1.replace(']', '')
                print("descripcion1 = ", descripcion1)

                # Fin  Consigo Id descripcion

                # Consigo Id tiposcomra

                miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                              password="BD_m3d1c4l")
                cur = miConexion.cursor()
                comando = "SELECT id FROM public.solicitud_tiposcompra WHERE nombre  = '" + tipo + "'"
                cur.execute(comando)
                print(comando)

                tipoId = []

                for id in cur.fetchall():
                    tipoId.append({'id': id})

                miConexion.close()

                print("dato")
                for dato in tipoId:
                    print(dato)
                    print(dato['id'])
                    print(json.dumps(dato['id']))
                    tipo1 = json.dumps(dato['id'])

                print("tipo1 = ", tipo1)
                tipo1 = tipo1.replace('[', '')
                tipo1 = tipo1.replace(']', '')
                print("tipo1 = ", tipo1)

                # Fin  Consigo Id tiposcomra

                # Consigo Id presentacion

                miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                              password="BD_m3d1c4l")
                cur = miConexion.cursor()
                comando = "SELECT id FROM public.solicitud_presentacion WHERE nombre  = '" + presentacion + "'"
                cur.execute(comando)
                print(comando)

                presentacionId = []

                for id in cur.fetchall():
                    presentacionId.append({'id': id})

                miConexion.close()

                print("dato")
                for dato in presentacionId:
                    print(dato)
                    print(dato['id'])
                    print(json.dumps(dato['id']))
                    presentacion1 = json.dumps(dato['id'])

                print("presentacion1 = ", presentacion1)
                presentacion1 = presentacion1.replace('[', '')
                presentacion1 = presentacion1.replace(']', '')

                print("presentacion1 DEFINITIVA = ", presentacion1)

                # Fin  Consigo Id presentacion

                ### Aqui fion busca Id pensientes

                miConexionu = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                              password="BD_m3d1c4l")
                curu = miConexionu.cursor()

                #comando = "INSERT INTO solicitud_solicitudesdetalle ( item ,  cantidad ,  justificacion ,  'especificacionesTecnicas' ,  'especificacionesAlmacen' ,  'observacionesCompras' ,  estadoreg ,             descripcion_id, 'estadosAlmacen_id', 'estadosCompras_id', 'estadosSolicitud_id', 'estadosValidacion_id', solicitud_id, 'tiposCompra_id', 'usuarioResponsableValidacion_id', 'entregadoAlmacen', presentacion_id, 'solicitadoAlmacen' )         VALUES(" + str(item) + ", " + str(cantidad) + ", '" + str(justificacion) + "', '', '', '', 'A', " + descripcion1 + ", 1, 1, 1, 1, " + solicitudId + ", " + tipo1 + "," + usuario1 + ",0," + presentacion1+ ", 0)"
                comando = 'INSERT INTO solicitud_solicitudesdetalle ( item ,  cantidad ,  justificacion ,  "especificacionesTecnicas" ,  "especificacionesAlmacen" ,  "observacionesCompras" ,  estadoreg ,             descripcion_id, "estadosAlmacen_id", "estadosCompras_id", "estadosSolicitud_id", "estadosValidacion_id", solicitud_id, "tiposCompra_id", "usuarioResponsableValidacion_id", "entregadoAlmacen", presentacion_id, "solicitadoAlmacen", producto,"usuarioResponsableAlmacen_id","usuarioResponsableCompra_id" ,iva, "recibidoOrdenCantidad","recibidoOrdenValor", "solicitadoOrdenCantidad", "solicitadoOrdenValor", "valorUnitario" )  VALUES(' + str(item) + ', ' + str(cantidad) + ',' + "'" + str(justificacion) + "'" + ",''," + "''" + ",'',"  + "'A'" + ','  + str(descripcion1) + ', 1, 1, 1, 1, ' + str(solicitudId) + ', ' + str(tipo1) + ',null' + ',0,' + str(presentacion1) + ', 0,' + "'" + str(producto) + "'"  + ',null,null,0,0,0,0,0,0 '    +  '  )'

                print(comando)
                curu.execute(comando)
                miConexionu.commit()
                item=item+1
                miConexionu.close()

            # Fin Rutina Grabacion del detalle de la solicitud

    #Rutina envia correo electonico:


    #remitente = "adminbd@outlook.com"
    print("Entre correo1")
    remitente = "adminbd@clinicamedical.com.co"
    destinatario = "alberto_bernalf@yahoo.com.co"
    mensaje = "Pruebas solicitudes"
    email = EmailMessage()
    print("Entre correo2")
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Correo de prueba"
    email.set_content(mensaje)
    print("Entre correo3")
    #smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp = smtplib.SMTP("smtp.office365.com", port=587)
    smtp.starttls()
    print("Entre correo3.5")
    #smtp.login(remitente, "75AAbb??")
    #print("Entre correo4")
    #smtp.sendmail(remitente, destinatario, email.as_string())
    #print ("Correo Enviado")
    #smtp.quit()
    ## fin rutina correo electronico
    #print("salid de Correo Enviado")

    return HttpResponse('Solicitud creada No ' + str(solicitudId))

    #debe habes un POST

## DESDE AQUI SOLICITUDESDT


## FIN SOLICITUDESDT

def ValidacionConsulta(request , username, sedeSeleccionada, nombreUsuario, nombreSede, perfil):
    pass
    print ("Entre a consulta solicitud a validar");
    context = {}

    print("username = ", username)
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['solicitudesForm'] = solicitudesForm
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = "SELECT areas.id id ,areas.area  area FROM public.solicitud_areas areas, public.solicitud_sedesCompra sedes WHERE areas.estadoreg = 'A' and areas.sede_id = sedes.id and  sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"
    #Reemplazado
    #comando = "SELECT areas.codreg_area id ,areas.area  area FROM mae_areas areas, imhotep_sedes sedes WHERE areas.activo = 'S' and areas.sede = sedes.sede and sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"
    cur.execute(comando)
    print(comando)

    areas = []

    for id, area in cur.fetchall():
        areas.append({'id': id, 'area': area})

    miConexion.close()

    context['Areas'] = areas

    return render(request, "Reportes/ValidacionConsulta.html", context)


## Desde Aqui codigo para Consultas Solicitud


def SolicitudesConsulta(request, username, sedeSeleccionada, nombreUsuario, nombreSede, perfil):

    context = {}
    print ("username = " , username )

    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil

    # Combo de Areas

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")
    comando = "SELECT areas.id id ,areas.area  area FROM public.solicitud_areas areas, public.solicitud_sedesCompra sedes WHERE areas.estadoreg = 'A' and areas.sede_id = sedes.id and  sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"
    cur.execute(comando)
    print(comando)
    areas = []
    areas.append({'id': '', 'area': ''})

    for id, area in cur.fetchall():
        areas.append({'id': id, 'area': area})

    miConexion.close()

    context['Areas'] = areas

    # Fin Combo Areas


    print ("Entre Consulta solicitudes")


    return render(request, 'Reportes\SolicitudesConsulta.html', context )



def load_dataSolicitudesConsulta(request, data):
    print("Entre DE VERDAD load_dataSolicitudesConsulta ")

    #data = request.GET['data']
    print ("data = ", data)
    d = json.loads(data)
    #desdeFechaSolicitud = d['desdeFechaSolicitud']
    #hastaFechaSolicitud = d['hastaFechaSolicitud']

    username = d['username']
    nombreSede = d['nombreSede']
    nombreUsuario = d['nombreUsuario']
    sedeSeleccionada = d['sedeSeleccionada']
    solicitudId = d['solicitudId']
    perfil = d['perfil']

    #print("desdeFechaSolicitud = ", d['desdeFechaSolicitud'])
    #print("hastaFechaSolicitud = ", d['hastaFechaSolicitud'])
    print("voy a context0")
    # Ahora SolicitudDetalle
    print("voy a context1")
    context = {}
    print ("pase contex2")

    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['solicitudId'] = solicitudId
    #context['desdeFechaSolicitud'] = desdeFechaSolicitud
    #context['hastaFechaSolicitud'] = hastaFechaSolicitud
    context['Perfil'] = perfil

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres", password="BD_m3d1c4l")
    # cur = miConexion.cursor()

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")
    print("voy comando")
    #comando = 'SELECT sol0.id id,substring(to_char(sol0.fecha,' + "'" + 'yyyy-mm-dd' + "'" + '),1,10)  fecha,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id , usu.nom_usuario usuSolicitud FROM public.solicitud_solicitudes sol0, public.solicitud_solicitudesDetalle sol , public.solicitud_descripcioncompra des, public.solicitud_tiposcompra tip, public.solicitud_presentacion pres, public.solicitud_articulos art    , public.solicitud_usuarios usu , public.solicitud_estadosvalidacion est      WHERE sol0.fecha >= ' + "'" + desdeFechaSolicitud + "'" + ' and sol0.fecha <= ' + "'"  + hastaFechaSolicitud + "'" + '  and sol0.id = sol.solicitud_id and des.id = sol.descripcion_id and tip.id = sol."tiposCompra_id" and pres.id = sol.presentacion_id and art."codregArticulo" = sol.producto and usu.num_identificacion = ' + "'" + str(username) + "'" + ' AND usu.id = sol0."usuarios_id" and est.id = sol."estadosValidacion_id"  ORDER BY sol0.fecha, sol.item'

    #comando = 'SELECT sol0.id id,substring(to_char(sol0.fecha,' + "'" + 'yyyy-mm-dd' + "'" + '),1,10)  fecha,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id , usu.nom_usuario usuSolicitud FROM public.solicitud_solicitudes sol0 LEFT JOIN public.solicitud_solicitudesDetalle sol ON (sol.solicitud_id = sol0.id ) LEFT JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id) LEFT JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id") LEFT JOIN public.solicitud_presentacion pres ON (pres.id = sol.presentacion_id) LEFT JOIN public.solicitud_articulos art ON (art."codregArticulo" = sol.producto ) LEFT JOIN public.solicitud_usuarios usu ON (usu.id = sol0."usuarios_id") LEFT JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id") WHERE sol0.fecha >= ' + "'" + desdeFechaSolicitud + "'" + ' and sol0.fecha <= ' + "'"  + hastaFechaSolicitud + "'" + ' and usu.num_identificacion = ' + "'" + str(username) + "' ORDER BY sol0.fecha, sol.item "
    comando = 'SELECT sol0.id id,substring(to_char(sol0.fecha,' + "'" + 'yyyy-mm-dd' + "'" + '),1,10)  fecha,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id , usu.nom_usuario usuSolicitud FROM public.solicitud_solicitudes sol0 LEFT JOIN public.solicitud_solicitudesDetalle sol ON (sol.solicitud_id = sol0.id ) LEFT JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id) LEFT JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id") LEFT JOIN public.solicitud_presentacion pres ON (pres.id = sol.presentacion_id) LEFT JOIN public.solicitud_articulos art ON (art."codregArticulo" = sol.producto ) LEFT JOIN public.solicitud_usuarios usu ON (usu.id = sol0."usuarios_id") LEFT JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id") WHERE usu.num_identificacion = ' + "'" + str(username) + "' ORDER BY sol0.fecha, sol.item "

    print("pase comando")
    cur.execute(comando)
    print(comando)

    solicitudDetalle = []


    for id, fecha, item, descripcion_id, descripcion, tipo, producto, nombre_producto, presentacion, cantidad, justificacion, tec, estValidacion, estadosValidacion_id, usuSolicitud in cur.fetchall():
        solicitudDetalle.append(
            {"model": "solicitud.solicitudesdetalle", "pk": id, "fields":
                {"id": id, "fecha":fecha, "item": item, "'descripcion_id": descripcion_id, "descripcion": descripcion,
                  "tiposCompra": tipo,
                "producto": producto, "nombre_producto": nombre_producto,
                "presentacion": presentacion, "cantidad": cantidad, "justificacion": justificacion,
             "especificacionesTecnicas": tec,
             "estadosValidacion": estValidacion, "estadosValidacion_id": estadosValidacion_id,
             "usuSolicitud": usuSolicitud}})

    miConexion.close()
    print("solicitudDetalle")
    print(solicitudDetalle)

    # Cierro Conexion

    context['SolicitudDetalle'] = solicitudDetalle

    ## Voy a enviar estadosSolicitudes

    # estadosvalidacionList = EstadosValidacion.objects.all()

    # json1 = serializers.serialize('json', estadosvalidacionList)
    serialized1 = json.dumps(solicitudDetalle)

    print("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')

class PostStoreSolicitudesConsulta(TemplateView):
        form_class = solicitudesDetalleForm
        template_name = 'Reportes/SolicitudesConsultaTrae.html'

        def post(self, request):
            print("Entre a post de SolicitudesConsultas")

            context = {}

            return JsonResponse({'success': True, 'message': 'Solicitud Detalle Created Successfully!'})

        def get_context_data(self, **kwargs):
            print("ENTRE POR EL GET_CONTEXT DEL VIEW de PostStoreSolicitudesConsulta : ")

            context = super().get_context_data(**kwargs)
            username = self.kwargs['username']
            sedeSeleccionada = self.kwargs['sedeSeleccionada']
            nombreUsuario = self.kwargs['nombreUsuario']
            nombreSede = self.kwargs['nombreSede']
            perfil =  self.kwargs['perfil']
            print("username =", username)
            print("sedeSeleccionada =", sedeSeleccionada)
            print("nombreUsuario =", nombreUsuario)
            print("nombreSede =", nombreSede)

            context['Username'] = username
            context['SedeSeleccionada'] = sedeSeleccionada
            context['NombreUsuario'] = nombreUsuario
            context['NombreSede'] = nombreSede
            context['Perfil'] = perfil
            #context['SolicitudId'] = solicitudId
            #desdeFechaSolicitud = self.request.GET['desdeFechaSolicitud']
            #hastaFechaSolicitud = self.request.GET['hastaFechaSolicitud']

            #print("desdeFechaSolicitud = ", desdeFechaSolicitud)
            #print("hastaFechaSolicitud = ", hastaFechaSolicitud)

            #context['DesdeFechaSolicitud'] = desdeFechaSolicitud
            #context['HastaFechaSolicitud'] = hastaFechaSolicitud

            return context

    ## Fin Desde Aqui codigo para Consultas Solicitud


# Create your views here.
def load_dataValidacion(request, data):
    print ("Entre load_data")

    context = {}
    d = json.loads(data)

    sedeSeleccionada = d['sedeSeleccionada']
    solicitudId = d['solicitudId']
    username = d['username']
    nombreUsuario = d['nombreUsuario']
    solicitudId = d['solicitudId']
    nombreSede = d['nombreSede']
    perfil = d['perfil']

    #print("data = ", request.GET('data'))

    #solicitudesDetalleList = SolicitudesDetalle.objects.all().filter(solicitud_id=solicitudId)

    # Ahora SolicitudDetalle

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    # cur = miConexion.cursor()

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")

    #comando = 'SELECT sol0.id solicitudNo,to_char(sol0.fecha,' + "'YYYY - MM - DD HH: MM.SS'" +  ') fecha, sol0.area_id area, areas.area nombre_area, sol0.usuarios_id idUsuarioCreaSol, usuariosCreaSol.nom_usuario usuariosCreaSol, sol.id id, sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo, sol.producto producto, art.articulo nombre_producto, pres.nombre  presentacion, sol.cantidad, sol.justificacion, sol."especificacionesTecnicas" tec, usu.nom_usuario usuResp, est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id FROM public.solicitud_solicitudes sol0, public.solicitud_solicitudesDetalle sol, public.solicitud_descripcioncompra des, public.solicitud_tiposcompra tip, public.solicitud_presentacion pres, public.solicitud_articulos art, public.solicitud_usuarios usu, public.solicitud_estadosvalidacion est, public.solicitud_areas areas, public.solicitud_usuarios usuariosCreaSol WHERE sol0.id = sol.solicitud_id AND sol0.estadoReg = '  + "'A" + "'" + ' AND des.id = sol.descripcion_id and tip.id = sol."tiposCompra_id" and pres.id = sol.presentacion_id and art."codregArticulo" = sol.producto and usu.id = sol."usuarioResponsableValidacion_id" and est.id = sol."estadosValidacion_id" and sol."estadosValidacion_id" = 1 and  areas.id = sol0.area_id and usuariosCreaSol.id = sol0.usuarios_id ORDER BY sol.item'
    comando = 'SELECT sol0.id solicitudNo,to_char(sol0.fecha,' + "'YYYY - MM - DD HH: MM.SS'" +  ') fecha, sol0.area_id area, areas.area nombre_area, sol0.usuarios_id idUsuarioCreaSol, usuariosCreaSol.nom_usuario usuariosCreaSol, sol.id id, sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo, sol.producto producto, art.articulo nombre_producto, pres.nombre  presentacion, sol.cantidad, sol.justificacion, sol."especificacionesTecnicas" tec, usu.nom_usuario usuResp, est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id FROM public.solicitud_solicitudes sol0 inner join public.solicitud_solicitudesDetalle sol on (sol.solicitud_id = sol0.id) inner join public.solicitud_descripcioncompra des on(des.id = sol.descripcion_id ) inner join public.solicitud_tiposcompra tip on (tip.id = sol."tiposCompra_id" ) inner join public.solicitud_presentacion pres on (pres.id = sol.presentacion_id ) inner join public.solicitud_articulos art on (art."codregArticulo" = sol.producto) left join public.solicitud_usuarios usu on (usu.id = sol."usuarioResponsableValidacion_id") inner join public.solicitud_estadosvalidacion est on (est.id = sol."estadosValidacion_id") inner join public.solicitud_areas areas on (areas.id = sol0.area_id) inner join public.solicitud_usuarios usuariosCreaSol on (usuariosCreaSol.id = sol0.usuarios_id) WHERE sol0.estadoReg = ' + "'A'" + ' AND sol."estadosValidacion_id" = 1 ORDER BY sol.item'
    cur.execute(comando)
    print(comando)

    solicitudDetalle = []
    #solicitudDetalle.append({"model":"solicitud.solicitudesdetalle"})

    if (perfil=='V'):

      for solicitudNo,fecha,area,nombre_area,idUsuarioCreaSol,usuariosCreaSol,  id, item, descripcion_id, descripcion, tipo, producto, nombre_producto, presentacion, cantidad, justificacion, tec, usuResp, estValidacion, estadosValidacion_id in cur.fetchall():
          solicitudDetalle.append(
            {"model":"solicitud.solicitudesdetalle","pk":id,"fields":
            {"solicitudNo":solicitudNo,"fecha":fecha,"area":area, "nombre_area":nombre_area,"idUsuarioCreaSol":idUsuarioCreaSol,"usuariosCreaSol":usuariosCreaSol,
            "id": id, "item": item, "'descripcion_id": descripcion_id, "descripcion": descripcion, "tiposCompra": tipo,
             "producto": producto,"nombre_producto": nombre_producto,
             "presentacion": presentacion, "cantidad": cantidad, "justificacion": justificacion, "especificacionesTecnicas": tec,
             "usuarioResponsableValidacion": usuResp, "estadosValidacion": estValidacion, "estadosValidacion_id": estadosValidacion_id}})

    miConexion.close()
    print("solicitudDetalle")
    print(solicitudDetalle)

    # Cierro Conexion

    #{"model": "solicitud.solicitudesdetalle", "pk": 6, "fields":

    context['SolicitudDetalle'] = solicitudDetalle

    ## Voy a enviar estadosSolicitudes

    #estadosvalidacionList = EstadosValidacion.objects.all()

    #json1 = serializers.serialize('json', estadosvalidacionList)
    serialized1 = json.dumps(solicitudDetalle)

    print ("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')


class PostStoreValidacion(TemplateView):
    form_class = solicitudesDetalleForm
    template_name = 'Reportes/ValidacionTraeU.html'

    def post(self, request):
        print ("Entre a Grabar")

        context = {}

        print("OPS Entre pos POST DEL VIEW Validacion")

        username = request.POST["username"]
        nombreSede = request.POST["nombreSede"]
        nombreUsuario = request.POST["nombreUsuario"]
        sedeSeleccionada = request.POST["sedeSeleccionada"]
        solicitudId = request.POST["solicitudId"]
        perfil = request.POST["perfil"]

        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = nombreUsuario
        context['NombreSede'] = nombreSede
        context['solicitudId'] = solicitudId
        context['Perfil'] = perfil
        print ("CONTEXTO solicitudId", solicitudId)

        form = self.form_class(request.POST)
        print ("Antes del Error :")
        print ("form = " , form)
        data = {'error': form.errors}
        print ("DATA MALUCA = ", data)

        if form.is_valid():
            try:
                print ("Entre forma valida")

                estadosValidacionAct = request.POST.get('estadosValidacion')
                especificacionesTecnicasAct = request.POST.get('especificacionesTecnicas')

                ## AVERIGUAMOS EL ID DEL USUARIO

                miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                              password="BD_m3d1c4l")
                cur = miConexion.cursor()

                comando = "SELECT id idActual FROM solicitud_usuarios WHERE num_identificacion = '" + str(username) + "'"
                print(comando)
                cur.execute(comando)
                idActualActual = []

                for idActual in cur.fetchall():
                    idActualActual.append({'idActual': idActual})

                print("idActual =", idActual)

                for dato in idActualActual:
                    print(dato)
                    print(dato['idActual'])
                    print(json.dumps(dato['idActual']))
                    idActual = json.dumps(dato['idActual'])

                idActual = idActual.replace('[', '')
                idActual = idActual.replace(']', '')
                print("idActual FINAL = ", idActual)

                miConexion.close()

                ## FIN AVERIGIAMOS ID DE USUARIO
                usuarioResponsableValidacion_idAct = idActual

                print ("estadosValidacionAct = ",estadosValidacionAct )
                print("especificacionesTecnicasAct = ", especificacionesTecnicasAct)
                print("usuarioResponsableValidacion_idAct = ", usuarioResponsableValidacion_idAct)
                pk = request.POST.get('pk')
                print("pk = ", pk)

                obj = get_object_or_404(SolicitudesDetalle, id=request.POST.get('pk'))
                estadosValidacionAnt = obj.estadosValidacion
                especificacionesTecnicasAnt = obj.especificacionesTecnicas
                usuarioResponsableValidacion_idAnt = obj.usuarioResponsableValidacion_id

                if (str(especificacionesTecnicasAnt) != str(especificacionesTecnicasAct) or str(estadosValidacionAnt) != str(estadosValidacionAct)):

                    obj.estadosValidacion = EstadosValidacion.objects.get(id=estadosValidacionAct)
                    obj.especificacionesTecnicas=especificacionesTecnicasAct
                    obj.usuarioResponsableValidacion_id = usuarioResponsableValidacion_idAct
                    obj.save()

                return JsonResponse({'success': True, 'message': 'Solicitud Detalle Updated Successfully!'})
            except:
                if (str(especificacionesTecnicasAnt) != str(especificacionesTecnicasAct) or str(estadosValidacionAnt) != str(estadosValidacionAct)):

                    obj.estadosValidacion = EstadosValidacion.objects.get(id=estadosValidacionAct)
                    obj.especificacionesTecnicas=especificacionesTecnicasAct
                    obj.usuarioResponsableValidacion_id = usuarioResponsableValidacion_idAct
                    obj.save()

                return JsonResponse({'success': True, 'message': 'Solicitud Detalle Created Successfully!'})
        else:
            return JsonResponse({'error': True, 'error': form.errors})
        return render(request, self.template_name,{'data':data})

    def get_context_data(self, **kwargs):
        print("ENTRE POR EL GET_CONTEXT DEL VIEW DE VALIDACION")


        username = self.kwargs['username']
        sedeSeleccionada = self.kwargs['sedeSeleccionada']
        nombreUsuario = self.kwargs['nombreUsuario']
        nombreSede = self.kwargs['nombreSede']
        perfil = self.kwargs['perfil']


        print("username =", username)
        print("sedeSeleccionada =", sedeSeleccionada)
        print("nombreUsuario =", nombreUsuario)
        print("nombreSede =", nombreSede)


        #context = super(PostStore, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = nombreUsuario
        context['NombreSede'] = nombreSede
        #context['SolicitudId'] = solicitudId
        context['Perfil'] = perfil

        #DESDE AQUIP

        # Buscamos estadosValidacion

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosValidacion est'
        cur.execute(comando)
        print(comando)

        estadosValidacion = []

        for id, nombre in cur.fetchall():
            estadosValidacion.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosValidacion")
        print(estadosValidacion)

        context['EstadosValidacion'] = estadosValidacion

        # Fin buscamos estdos validacion

        # Buscamos la solicitud

        return context


        #HASTA AQUIP


def post_editValidacion(request,id,username,sedeSeleccionada,nombreUsuario,nombreSede,perfil,solicitudId):
    print ("Entre POST edit")
    print ("id = " , id)

    print ("username =" , username)
    print("sedeSeleccionada =", sedeSeleccionada)
    print("nombreUsuario =", nombreUsuario)
    print("nombreSede =", nombreSede)
    print("solicitudId =", solicitudId)

    context = {}
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['solicitudId'] = solicitudId
    context['Perfil'] = perfil



    if request.method == 'GET':

        #solicitudesDetalle = SolicitudesDetalle.objects.filter(id=id).first()

        # Abro Conexion

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        # cur = miConexion.cursor()

        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")


        #comando = 'SELECT sol.id id,sol.item item, sol.descripcion_id descripcion_id, des.nombre descripcion,sol."tiposCompra_id" tiposCompra_id, tip.nombre tipo , sol.producto producto, substring(art.articulo,1,150) nombre_producto ,sol.presentacion_id  presentacion_id, pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, sol."usuarioResponsableValidacion_id" usuarioResponsableValidacion_id,  usu.nom_usuario usuResp  , est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id  FROM public.solicitud_solicitudesDetalle sol , public.solicitud_descripcioncompra des, public.solicitud_tiposcompra tip, public.solicitud_presentacion pres, public.solicitud_articulos art    , public.solicitud_usuarios usu , public.solicitud_estadosvalidacion est  WHERE sol.id = ' + str(id) + ' AND des.id = sol.descripcion_id and tip.id = sol."tiposCompra_id" and pres.id = sol.presentacion_id and art."codregArticulo" = sol.producto and usu.id = sol."usuarioResponsableValidacion_id" and est.id = sol."estadosValidacion_id" ORDER BY sol.item'
        comando = 'SELECT sol.id id,sol.item item, sol.descripcion_id descripcion_id, des.nombre descripcion,sol."tiposCompra_id" tiposCompra_id, tip.nombre tipo , sol.producto producto, substring(art.articulo,1,150) nombre_producto ,sol.presentacion_id  presentacion_id, pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, sol."usuarioResponsableValidacion_id" usuarioResponsableValidacion_id,  usu.nom_usuario usuResp  , est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id  FROM public.solicitud_solicitudesDetalle sol INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id) INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id") INNER JOIN public.solicitud_presentacion pres ON (pres.id = sol.presentacion_id) INNER JOIN public.solicitud_articulos art ON (art."codregArticulo" = sol.producto) LEFT JOIN public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id")  WHERE sol.id = ' + str(id) + ' ORDER BY sol.item'

        cur.execute(comando)
        print(comando)

        solicitudDetalle = []
        # solicitudDetalle.append({"model":"solicitud.solicitudesdetalle"})

        for id, item, descripcion_id, descripcion, tiposCompra_id, tipo, producto,nombre_producto, presentacion_id , presentacion, cantidad, justificacion, tec,usuarioResponsableValidacion_id, usuResp, estValidacion, estadosValidacion_id in cur.fetchall():
            solicitudDetalle.append(
                {
                    #"model": "solicitud.solicitudesdetalle", "pk": id, "fields": {
                     "id": id, "item": item, "descripcion_id": descripcion_id, "descripcion": descripcion,
                    "tiposCompra_id": tiposCompra_id, "tiposCompra": tipo,
                     "producto": producto,"nombre_producto": nombre_producto,
                    "presentacion_id": presentacion_id,
                     "presentacion": presentacion, "cantidad": cantidad, "justificacion": justificacion,
                     "especificacionesTecnicas": tec,
                    "usuarioResponsableValidacion_id": usuarioResponsableValidacion_id,
                     "usuarioResponsableValidacion": usuResp, "estadosValidacion": estValidacion,
                     "estadosValidacion_id": estadosValidacion_id#}
                })

        miConexion.close()
        print("solicitudDetalle")
        print(solicitudDetalle)

        # Cierro Conexion


        print ("Me devuelvo a la MODAL")

        return JsonResponse({'pk':solicitudDetalle[0]['id'],'item':solicitudDetalle[0]['item'],
                             'descripcion_id': solicitudDetalle[0]['descripcion_id'],
                             'descripcion':solicitudDetalle[0]['descripcion'],'tiposCompra_id':solicitudDetalle[0]['tiposCompra_id'], 'tiposCompra':solicitudDetalle[0]['tiposCompra'],
                             'producto':solicitudDetalle[0]['producto'],
                             'nombre_producto': solicitudDetalle[0]['nombre_producto'],
                             'presentacion_id': solicitudDetalle[0]['presentacion_id'],
                             'presentacion':solicitudDetalle[0]['presentacion'],
                             'cantidad':solicitudDetalle[0]['cantidad'],'justificacion':solicitudDetalle[0]['justificacion'],
                             'especificacionesTecnicas':solicitudDetalle[0]['especificacionesTecnicas'],
                             'usuarioResponsableValidacion_id': solicitudDetalle[0]['usuarioResponsableValidacion_id'],
                             'usuarioResponsableValidacion':solicitudDetalle[0]['usuarioResponsableValidacion'],
                             'estadosValidacion':solicitudDetalle[0]['estadosValidacion'],'estadosValidacion_id': solicitudDetalle[0]['estadosValidacion_id'] })
    else:
        return JsonResponse({'errors':'Something went wrong!'})

def post_deleteValidacion(request,id):
    print ("Entre a borrar")
    solicitudesDetalle = SolicitudesDetalle.objects.get(id=id)
    solicitudesDetalle.delete()
    return HttpResponseRedirect(reverse('index'))

# Fin Create your views here. para validacion


# Create your views here. para Almacen
def AlmacenConsulta(request , username, sedeSeleccionada, nombreUsuario, nombreSede, perfil) :
    pass
    print("Entre a consulta Solicitudes a Almacen");
    context = {}

    print("username = ", username)
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['solicitudesForm'] = solicitudesForm
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = "SELECT areas.id id ,areas.area area FROM PUBLIC.solicitud_areas areas, public.solicitud_sedesCompra sedes WHERE areas.estadoreg = 'A' and areas.sede_id = sedes.id and  sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"


    print(comando)
    cur.execute(comando)

    areas = []

    for id, area in cur.fetchall():
        areas.append({'id': id, 'area': area})

    miConexion.close()

    context['Areas'] = areas

    print(" Envio NombreSede = ",  context['NombreSede'])

    return render(request, "Reportes/AlmacenConsulta.html", context)


class PostStoreAlmacen(TemplateView):
    form_class = solicitudesDetalleForm
    template_name = 'Reportes/AlmacenTraeU.html'

    def post(self, request):
        print ("Entre a Grabar almacen")

        context = {}

        print("OPS Entre pos POST DEL VIEW")

        username = request.POST["username"]
        nombreSede = request.POST["nombreSede"]
        nombreUsuario = request.POST["nombreUsuario"]
        sedeSeleccionada = request.POST["sedeSeleccionada"]
        solicitudId = request.POST["solicitudId"]
        perfil = request.POST["perfil"]


        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = nombreUsuario
        context['NombreSede'] = nombreSede
        context['solicitudId'] = solicitudId
        context['Perfil'] = perfil

        print ("CONTEXTO solicitudId", solicitudId)

        form = self.form_class(request.POST)

        data = {'error': form.errors}
        print ("DATA MALUCA = ", data)

        if form.is_valid():
            try:
                print ("Entre forma valida")

                estadosAlmacenAct = request.POST.get('estadosAlmacen')
                especificacionesAlmacenAct = request.POST.get('especificacionesAlmacen')

                ## AVERIGUAMOS EL ID DEL USUARIO

                miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                              password="BD_m3d1c4l")
                cur = miConexion.cursor()

                comando = "SELECT id idActual FROM solicitud_usuarios WHERE num_identificacion = '" + str(username) + "'"
                print(comando)
                cur.execute(comando)
                idActualActual = []

                for idActual in cur.fetchall():
                    idActualActual.append({'idActual': idActual})

                print("idActual =", idActual)

                for dato in idActualActual:
                    print(dato)
                    print(dato['idActual'])
                    print(json.dumps(dato['idActual']))
                    idActual = json.dumps(dato['idActual'])

                idActual = idActual.replace('[', '')
                idActual = idActual.replace(']', '')
                print("idActual FINAL = ", idActual)

                miConexion.close()

                ## FIN AVERIGIAMOS ID DE USUARIO
                usuAlmacenAct = idActual

                print ("estadosAlmacenAct = ",estadosAlmacenAct )
                print("especificacionesAlmacenAct = ", especificacionesAlmacenAct)
                print("usuAlmacenAct = ", usuAlmacenAct)
                pk = request.POST.get('pk')
                print("pk = ", pk)

                obj = get_object_or_404(SolicitudesDetalle, id=request.POST.get('pk'))
                estadosAlmacenAnt = obj.estadosAlmacen
                especificacionesAlmacenAnt = obj.especificacionesAlmacen
                usuAlmacenAnt = obj.usuarioResponsableAlmacen_id

                if (str(especificacionesAlmacenAnt) != str(especificacionesAlmacenAct) or str(estadosAlmacenAnt) != str(estadosAlmacenAct)):

                    obj.estadosAlmacen_id = EstadosValidacion.objects.get(id=estadosAlmacenAct)
                    obj.especificacionesAlmacen=especificacionesAlmacenAct
                    obj.usuarioResponsableAlmacen_id = usuAlmacenAct
                    obj.save()

                return JsonResponse({'success': True, 'message': 'Solicitud Detalle Updated Successfully!'})
            except:
                if (str(especificacionesTecnicasAnt) != str(especificacionesTecnicasAct) or str(estadosValidacionAnt) != str(estadosValidacionAct)):
                    obj.estadosAlmacen_id = EstadosValidacion.objects.get(id=estadosAlmacenAct)
                    obj.especificacionesAlmacen = especificacionesAlmacenAct
                    obj.usuarioResponsableAlmacen_id = usuAlmacenAct
                    obj.save()

                return JsonResponse({'success': True, 'message': 'Solicitud Detalle Created Successfully!'})
        else:
            return JsonResponse({'error': True, 'error': form.errors})
        return render(request, self.template_name,{'data':data})

    def get_context_data(self, **kwargs):
        print("ENTRE POR EL GET_CONTEXT DEL VIEW  de almacen")
        context = super().get_context_data(**kwargs)

        username = self.kwargs['username']
        sedeSeleccionada = self.kwargs['sedeSeleccionada']
        nombreUsuario = self.kwargs['nombreUsuario']
        nombreSede = self.kwargs['nombreSede']
        perfil = self.kwargs['perfil']


        print("username =", username)
        print("sedeSeleccionada =", sedeSeleccionada)
        print("nombreUsuario =", nombreUsuario)
        print("nombreSede =", nombreSede)


        #context = super(PostStore, self).get_context_data(**kwargs)

        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = nombreUsuario
        context['NombreSede'] = nombreSede

        context['Perfil'] = perfil

        #DESDE AQUIP

        # Buscamos estadosValidacion

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosValidacion est'
        cur.execute(comando)
        print(comando)

        estadosValidacion = []

        for id, nombre in cur.fetchall():
            estadosValidacion.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosValidacion")
        print(estadosValidacion)

        context['EstadosValidacion'] = estadosValidacion

        # Fin buscamos estdos validacion

        # Buscamos estadosAlmacen

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosAlmacen est'
        cur.execute(comando)
        print(comando)

        estadosAlmacen = []

        for id, nombre in cur.fetchall():
            estadosAlmacen.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosAlmacen")
        print(estadosAlmacen)

        context['EstadosAlmacen'] = estadosAlmacen

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()
        comando = "SELECT areas.id id ,areas.area area FROM PUBLIC.solicitud_areas areas, public.solicitud_sedesCompra sedes WHERE areas.estadoreg = 'A' and areas.sede_id = sedes.id and  sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"

        print(comando)
        cur.execute(comando)

        areas = []

        for id, area in cur.fetchall():
            areas.append({'id': id, 'area': area})

        miConexion.close()

        context['Areas'] = areas

        # Fin buscamos estados Almacen

        return context


        #HASTA AQUIP class PostStoreAlmacen

def load_dataAlmacen(request, data):
    print("Entre load_data = ", data)

    context = {}
    d = json.loads(data)

    sedeSeleccionada = d['sedeSeleccionada']
    solicitudId = d['solicitudId']
    username = d['username']
    nombreUsuario = d['nombreUsuario']
    solicitudId = d['solicitudId']
    nombreSede = d['nombreSede']
    perfil = d['perfil']


    #solicitudesDetalleList = SolicitudesDetalle.objects.all().filter(solicitud_id=solicitudId)

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")


    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")


    #comando = 'SELECT sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,usu.nom_usuario usuResp  , est.nombre estValidacion, est1.nombre estadosAlmacen, sol."estadosValidacion_id" estadosValidacion_id, sol."especificacionesAlmacen" especificacionesAlmacen, sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen FROM public.solicitud_solicitudesDetalle sol INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id) INNER JOIN public.solicitud_articulos art   ON (art."codregArticulo" = sol.producto) LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) INNER JOIN public.solicitud_estadosvalidacion est1  ON (est1.id = sol."estadosAlmacen_id") WHERE sol.solicitud_id = ' + solicitudId + ' ORDER BY sol.item '
    comando = 'SELECT sol0.id solicitudNo,to_char(sol0.fecha,' + "'YYYY - MM - DD HH: MM.SS'" + ') fecha, sol0.area_id area, areas.area nombre_area, sol0.usuarios_id idUsuarioCreaSol , usuariosCreaSol.nom_usuario usuariosCreaSol, sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,usu.nom_usuario usuResp  , est.nombre estValidacion, est1.nombre estadosAlmacen, sol."estadosValidacion_id" estadosValidacion_id, sol."especificacionesAlmacen" especificacionesAlmacen,sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen FROM public.solicitud_solicitudes sol0 INNER JOIN public.solicitud_solicitudesDetalle sol on (sol.solicitud_id=sol0.id) INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id) INNER JOIN public.solicitud_articulos art   ON (art."codregArticulo" = sol.producto) LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) INNER JOIN public.solicitud_estadosAlmacen est1  ON (est1.id = sol."estadosAlmacen_id") inner join public.solicitud_areas areas on (areas.id = sol0.area_id) inner join public.solicitud_usuarios usuariosCreaSol on (usuariosCreaSol.id = sol0.usuarios_id) WHERE  sol0.estadoReg = ' + "'A'" + ' AND sol."estadosAlmacen_id" = 1 ORDER BY sol.item '


    cur.execute(comando)
    print(comando)

    solicitudDetalle = []
    # solicitudDetalle.append({"model":"solicitud.solicitudesdetalle"})

    if (perfil == 'A'):
      for solicitudNo,fecha,area,nombre_area,idUsuarioCreaSol,usuariosCreaSol,id, item, descripcion_id, descripcion, tipo, producto, nombre_producto, presentacion, cantidad, justificacion, tec, usuResp, estValidacion, estadosAlmacen, estadosValidacion_id, especificacionesAlmacen, estadosAlmacen_id, usuAlmacen in cur.fetchall():
        solicitudDetalle.append(
            {"model": "solicitud.solicitudesdetalle", "pk": id, "fields":
                {"solicitudNo":solicitudNo,"fecha":fecha,"area":area, "nombre_area":nombre_area,"idUsuarioCreaSol":idUsuarioCreaSol,"usuariosCreaSol":usuariosCreaSol,
                    "id": id, "item": item, "'descripcion_id": descripcion_id, "descripcion": descripcion,
                 "tiposCompra": tipo,
                 "producto": producto, "nombre_producto": nombre_producto,
                 "presentacion": presentacion, "cantidad": cantidad, "justificacion": justificacion,
                 "especificacionesTecnicas": tec,
                 "usuarioResponsableValidacion": usuResp, "estadosValidacion": estValidacion,
                 "estadosAlmacen": estadosAlmacen,
                 "estadosValidacion_id": estadosValidacion_id,
                 "especificacionesAlmacen": especificacionesAlmacen, "estadosAlmacen_id": estadosAlmacen_id,
                 "usuAlmacen": usuAlmacen
                 }})

    miConexion.close()
    print("solicitudDetalle")
    print(solicitudDetalle)

    # Cierro Conexion

    # {"model": "solicitud.solicitudesdetalle", "pk": 6, "fields":

    context['SolicitudDetalle'] = solicitudDetalle
    #solicitudDetalle.append("sedeSeleccionada", sedeSeleccionada)

    serialized1 = json.dumps(solicitudDetalle)

    print("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')



def post_editAlmacen(request,id,username,sedeSeleccionada,nombreUsuario,nombreSede,perfil,solicitudId):
    print ("Entre POST edit ALMACEN")
    print ("id = " , id)
    identif = id

    print ("username =" , username)
    print("sedeSeleccionada =", sedeSeleccionada)
    print("nombreUsuario =", nombreUsuario)
    print("nombreSede =", nombreSede)
    print("solicitudId =", solicitudId)

    context = {}
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['solicitudId'] = solicitudId
    context['Perfil'] = perfil


    if request.method == 'GET':

        #solicitudesDetalle = SolicitudesDetalle.objects.filter(id=id).first()

        # Abro Conexion

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        # cur = miConexion.cursor()

        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        #comando = 'SELECT sol.id id ,sol.item item, sol.descripcion_id descripcion_id, des.nombre descripcion,sol."tiposCompra_id" tiposCompra_id, tip.nombre tipo , sol.producto producto, substring(art.articulo,1,150) nombre_producto ,sol.presentacion_id  presentacion_id, pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, sol."usuarioResponsableValidacion_id" usuarioResponsableValidacion_id,  usu.nom_usuario usuResp  , est.nombre estValidacion,est1.nombre estadosAlmacen  , sol."estadosValidacion_id" estadosValidacion_id ,  sol."especificacionesAlmacen" especificacionesAlmacen, sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen    FROM public.solicitud_solicitudesDetalle sol , public.solicitud_descripcioncompra des, public.solicitud_tiposcompra tip, public.solicitud_presentacion pres, public.solicitud_articulos art    , public.solicitud_usuarios usu , public.solicitud_usuarios usu1 , public.solicitud_estadosvalidacion est, public.solicitud_estadosvalidacion est1   WHERE sol.id = ' + str(id) + ' AND des.id = sol.descripcion_id and tip.id = sol."tiposCompra_id" and pres.id = sol.presentacion_id and art."codregArticulo" = sol.producto and usu1.id = sol."usuarioResponsableAlmacen_id" and usu.id = sol."usuarioResponsableValidacion_id" and est1.id = sol."estadosAlmacen_id"  and est.id = sol."estadosValidacion_id" ORDER BY sol.item'
        comando =  'SELECT sol.id id ,sol.item item, sol.descripcion_id descripcion_id, des.nombre descripcion,sol."tiposCompra_id" tiposCompra_id, tip.nombre tipo , sol.producto producto, substring(art.articulo,1,150) nombre_producto ,sol.presentacion_id  presentacion_id, pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, sol."usuarioResponsableValidacion_id" usuarioResponsableValidacion_id,  usu.nom_usuario usuResp  , est.nombre estValidacion,est1.nombre estadosAlmacen  , sol."estadosValidacion_id" estadosValidacion_id ,  sol."especificacionesAlmacen" especificacionesAlmacen, sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen    FROM public.solicitud_solicitudesDetalle sol INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id) INNER JOIN public.solicitud_articulos art   ON (art."codregArticulo" = sol.producto) LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) INNER JOIN public.solicitud_estadosvalidacion est1  ON (est1.id = sol."estadosAlmacen_id") WHERE sol.id = ' + str(identif) + ' ORDER BY sol.item '
        cur.execute(comando)
        print(comando)

        solicitudDetalle = []
        # solicitudDetalle.append({"model":"solicitud.solicitudesdetalle"})

        for id, item, descripcion_id, descripcion, tiposCompra_id, tipo, producto,nombre_producto, presentacion_id , presentacion, cantidad, justificacion, tec,usuarioResponsableValidacion_id, usuResp, estValidacion,estadosAlmacen, estadosValidacion_id, especificacionesAlmacen, estadosAlmacen_id , usuAlmacen    in cur.fetchall():

            solicitudDetalle.append(
                {
                    #"model": "solicitud.solicitudesdetalle", "pk": id, "fields": {
                     "id": id, "item": item, "descripcion_id": descripcion_id, "descripcion": descripcion,
                    "tiposCompra_id": tiposCompra_id, "tiposCompra": tipo,
                     "producto": producto,"nombre_producto": nombre_producto,
                    "presentacion_id": presentacion_id,
                     "presentacion": presentacion, "cantidad": cantidad, "justificacion": justificacion,
                     "especificacionesTecnicas": tec,
                    "usuarioResponsableValidacion_id": usuarioResponsableValidacion_id,
                     "usuarioResponsableValidacion": usuResp, "estadosValidacion": estValidacion,
                     "estadosAlmacen": estadosAlmacen,
                     "estadosValidacion_id": estadosValidacion_id,
                    "especificacionesAlmacen":especificacionesAlmacen, "estadosAlmacen_id":estadosAlmacen_id,
                    "usuAlmacen":usuAlmacen
                           })

        miConexion.close()
        print("solicitudDetalle")
        print(solicitudDetalle)

        # Cierro Conexion


        print ("Me devuelvo a la MODAL")

        return JsonResponse({'pk':solicitudDetalle[0]['id'],'item':solicitudDetalle[0]['item'],
                             'descripcion_id': solicitudDetalle[0]['descripcion_id'],
                             'descripcion':solicitudDetalle[0]['descripcion'],'tiposCompra_id':solicitudDetalle[0]['tiposCompra_id'], 'tiposCompra':solicitudDetalle[0]['tiposCompra'],
                             'producto':solicitudDetalle[0]['producto'],
                             'nombre_producto': solicitudDetalle[0]['nombre_producto'],
                             'presentacion_id': solicitudDetalle[0]['presentacion_id'],
                             'presentacion':solicitudDetalle[0]['presentacion'],
                             'cantidad':solicitudDetalle[0]['cantidad'],'justificacion':solicitudDetalle[0]['justificacion'],
                             'especificacionesTecnicas':solicitudDetalle[0]['especificacionesTecnicas'],
                             'usuarioResponsableValidacion_id': solicitudDetalle[0]['usuarioResponsableValidacion_id'],
                             'usuarioResponsableValidacion':solicitudDetalle[0]['usuarioResponsableValidacion'],
                             'estadosValidacion':solicitudDetalle[0]['estadosValidacion'],
                             'estadosAlmacen': solicitudDetalle[0]['estadosAlmacen'],
                             'estadosValidacion_id': solicitudDetalle[0]['estadosValidacion_id'],
                             'especificacionesAlmacen':solicitudDetalle[0]['especificacionesAlmacen'],
                             'estadosAlmacen_id': solicitudDetalle[0]['estadosAlmacen_id'],
                             'usuAlmacen': solicitudDetalle[0]['usuAlmacen']
                             })
    else:
        return JsonResponse({'errors':'Something went wrong!'})

def post_deleteAlmacen(request,id):
    print ("Entre a borrar")
    solicitudesDetalle = SolicitudesDetalle.objects.get(id=id)
    solicitudesDetalle.delete()
    return HttpResponseRedirect(reverse('index'))



# Fin Create your views here. para Almacen


# Create your views here. para Compras

def ComprasConsulta(request , username, sedeSeleccionada, nombreUsuario, nombreSede, perfil) :
    pass
    print("Entre a consulta Solicitudes a Compras");
    context = {}

    print("username = ", username)
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['solicitudesForm'] = solicitudesForm
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = "SELECT areas.id id ,areas.area  area FROM public.solicitud_areas areas, public.solicitud_sedesCompra sedes WHERE areas.estadoreg = 'A' and areas.sede_id = sedes.id and  sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"
    # Reemplazado
    # comando = "SELECT areas.codreg_area id ,areas.area  area FROM mae_areas areas, imhotep_sedes sedes WHERE areas.activo = 'S' and areas.sede = sedes.sede and sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"
    cur.execute(comando)
    print(comando)

    areas = []

    for id, area in cur.fetchall():
        areas.append({'id': id, 'area': area})

    miConexion.close()

    context['Areas'] = areas

    return render(request, "Reportes/ComprasConsulta.html", context)

class PostStoreCompras(TemplateView):
    form_class = solicitudesDetalleForm
    template_name = 'Reportes/ComprasTraeU.html'

    def post(self, request):
      if request.is_ajax():

        print ("Entre a Grabar compras")
        context = {}
        print("OPS Entre pos POST DEL VIEW DE COMPRAS")

        username = request.POST["username"]
        nombreSede = request.POST["nombreSede"]
        nombreUsuario = request.POST["nombreUsuario"]
        sedeSeleccionada = request.POST["sedeSeleccionada"]
        solicitudId = request.POST["solicitudId"]
        perfil = request.POST["perfil"]

        print ("perfil = ", perfil)
        print ("username = ", username)
        print("sedeSeleccionada = ", sedeSeleccionada)

        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = nombreUsuario
        context['NombreSede'] = nombreSede
        context['solicitudId'] = solicitudId
        context['Perfil'] = perfil

        print ("CONTEXTO solicitudId", solicitudId)

        form = self.form_class(request.POST, request.FILES)

        files = self.form_class(request.FILES)
        print(" archivo = ", files)

        print ("Nombre del archivo = ", files['adjuntoCompras'])

        data = {'error': form.errors}
        print ("DATA MALUCA = ", data)

        if form.is_valid():
            try:
                print ("Entre forma valida COMPRASSS ... ")

                estadosComprasAct = request.POST.get('estadosCompras')
                observacionesComprasAct = request.POST.get('observacionesCompras')

                adjuntoComprasAct = form.files



                print ("adjuntoComprasAct = ", adjuntoComprasAct)

                nombreArchivo=""

                my_var = adjuntoComprasAct.get( 'adjuntoCompras', None)
                print ("my_var = ", my_var)


                #if self.form_class(request.FILES):
                if (my_var  == None):
                    print("Entre Nulo")
                    nombreArchivo = ""
                else:
                    print ("Entre No  Nulo")
                    print(" adjuntoComprasAct = ", adjuntoComprasAct)
                    nombreArchivo = adjuntoComprasAct['adjuntoCompras']
                    print("adjuntoComprasAct = ", adjuntoComprasAct['adjuntoCompras'])


                ## AVERIGUAMOS EL ID DEL USUARIO
                print ("PASE 0")
                miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                              password="BD_m3d1c4l")
                cur = miConexion.cursor()

                comando = "SELECT id idActual FROM solicitud_usuarios WHERE num_identificacion = '" + str(username) + "'"
                print(comando)
                cur.execute(comando)
                idActualActual = []

                print ("PASE 1")

                for idActual in cur.fetchall():
                    idActualActual.append({'idActual': idActual})

                print("idActual =", idActual)

                for dato in idActualActual:
                    print(dato)
                    print(dato['idActual'])
                    print(json.dumps(dato['idActual']))
                    idActual = json.dumps(dato['idActual'])

                idActual = idActual.replace('[', '')
                idActual = idActual.replace(']', '')
                print("idActual FINAL = ", idActual)

                miConexion.close()

                ## FIN AVERIGIAMOS ID DE USUARIO
                usuComprasAct = idActual

                print ("estadosComprasAct = ",estadosComprasAct )
                print("observacionesComprasAct = ", observacionesComprasAct)
                print("usuComprasAct = ", usuComprasAct)
                pk = request.POST.get('pk')
                print("pk = ", pk)
                print("Voy a guardar a forma")
                form.save()
                print("Forma  guardada")
                obj = get_object_or_404(SolicitudesDetalle, id=request.POST.get('pk'))
                estadosComprasAnt = obj.estadosCompras
                observacionesComprasAnt = obj.observacionesCompras
                usuComprasAnt = obj.usuarioResponsableCompra


                if (str(observacionesComprasAnt) != str(observacionesComprasAct) or str(estadosComprasAnt) != str(estadosComprasAct)):

                    obj.estadosCompras_id = EstadosValidacion.objects.get(id=estadosComprasAct)
                    obj.observacionesCompras=observacionesComprasAct
                    obj.usuarioResponsableCompra_id = usuComprasAct
                    obj.adjuntoCompras = nombreArchivo
                    obj.save()

                return JsonResponse({'success': True, 'message': 'Solicitud Detalle Updated Successfully!'})
            except:
                if (str(observacionesComprasAnt) != str(observacionesComprasAct) or str(estadosComprasAnt) != str(estadosComprasAct)):
                    print(" me voy por error")

                    obj.estadosCompras_id = EstadosValidacion.objects.get(id=estadosComprasAct)
                    obj.observacionesCompras = observacionesComprasAct
                    obj.usuarioResponsableCompra_id = usuComprasAct

                    obj.adjuntoCompras = nombreArchivo
                    obj.save()

                return JsonResponse({'success': True, 'message': 'Solicitud Detalle Created Successfully!'})
        else:
            return JsonResponse({'error': True, 'error': form.errors})
        return render(request, self.template_name,{'data':data})

    def get_context_data(self, **kwargs):
        print("ENTRE POR EL GET_CONTEXT DEL VIEW COMPRAS")
        username = self.kwargs['username']
        sedeSeleccionada = self.kwargs['sedeSeleccionada']
        nombreUsuario = self.kwargs['nombreUsuario']
        nombreSede = self.kwargs['nombreSede']
        perfil = self.kwargs['perfil']


        print("username =", username)
        print("sedeSeleccionada =", sedeSeleccionada)
        print("nombreUsuario =", nombreUsuario)
        print("nombreSede =", nombreSede)


        #context = super(PostStore, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)

        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = nombreUsuario
        context['NombreSede'] = nombreSede

        context['Perfil'] = perfil

        #DESDE AQUIP

        # Buscamos estadosValidacion

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosValidacion est'
        cur.execute(comando)
        print(comando)

        estadosValidacion = []

        for id, nombre in cur.fetchall():
            estadosValidacion.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosValidacion")
        print(estadosValidacion)

        context['EstadosValidacion'] = estadosValidacion

        # Fin buscamos estdos validacion

        # Buscamos estadosAlmacen

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosAlmacen est'
        cur.execute(comando)
        print(comando)

        estadosAlmacen = []

        for id, nombre in cur.fetchall():
            estadosAlmacen.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosAlmacen")
        print(estadosAlmacen)

        context['EstadosAlmacen'] = estadosAlmacen

        # Fin buscamos estados Almacen

        # Buscamos estadosCompras

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosValidacion est'
        cur.execute(comando)
        print(comando)

        estadosCompras = []

        for id, nombre in cur.fetchall():
            estadosCompras.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosCompras")
        print(estadosCompras)

        context['EstadosCompras'] = estadosCompras

        # Fin buscamos estados Almacen

        return context


        #HASTA AQUIP class PostStoreCompras

def load_dataCompras(request, data):

    print("Entre load_data de COMPRAS= ", data)
    context = {}
    print("pase0")
    d = json.loads(data)
    print("pase1")
    print("sedeSeleccionada  = ", d['sedeSeleccionada'])

    sedeSeleccionada = d['sedeSeleccionada']
    print("sedeSeleccionada = ", sedeSeleccionada)
    solicitudId = d['solicitudId']
    username = d['username']
    nombreUsuario = d['nombreUsuario']
    solicitudId = d['solicitudId']
    nombreSede = d['nombreSede']
    perfil = d['perfil']

    #print("data = ", request.GET('data'))

    #solicitudesDetalleList = SolicitudesDetalle.objects.all().filter(solicitud_id=solicitudId)

    # Ahora SolicitudDetalle
    context= {}

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    # cur = miConexion.cursor()

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")

    #comando =  'SELECT sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,usu.nom_usuario usuResp  , est.nombre estValidacion,est1.nombre estadosAlmacen, sol."estadosValidacion_id" estadosValidacion_id, sol."especificacionesAlmacen" especificacionesAlmacen, sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen , sol."observacionesCompras" observacionesCompras, sol."estadosCompras_id" estadosCompras_id, est2.nombre estadosCompras, usu2.nom_usuario usuCompras  FROM public.solicitud_solicitudesDetalle sol INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id) INNER JOIN public.solicitud_articulos art   ON (art."codregArticulo" = sol.producto) LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") LEFT JOIN public.solicitud_usuarios usu2 ON (usu2.id = sol."usuarioResponsableCompra_id") INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) INNER JOIN public.solicitud_estadosvalidacion est1  ON (est1.id = sol."estadosAlmacen_id")  INNER JOIN public.solicitud_estadosvalidacion est2  ON (est2.id = "estadosCompras_id") WHERE sol.solicitud_id = ' + solicitudId + ' ORDER BY sol.item '
    comando = 'SELECT sol0.id solicitudNo,to_char(sol0.fecha,' + "'YYYY - MM - DD HH: MM.SS'" + ') fecha, sol0.area_id area, areas.area nombre_area, sol0.usuarios_id idUsuarioCreaSol , usuariosCreaSol.nom_usuario usuariosCreaSol, sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,usu.nom_usuario usuResp  , est.nombre estValidacion,est1.nombre estadosAlmacen, sol."estadosValidacion_id" estadosValidacion_id, sol."especificacionesAlmacen" especificacionesAlmacen, sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen , sol."observacionesCompras" observacionesCompras, sol."estadosCompras_id" estadosCompras_id, est2.nombre estadosCompras, usu2.nom_usuario usuCompras , sol."adjuntoCompras"  adjuntoCompras  FROM public.solicitud_solicitudes sol0 INNER JOIN public.solicitud_solicitudesDetalle sol ON (sol.solicitud_id = sol0.id) INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id)  INNER JOIN public.solicitud_articulos art ON (art."codregArticulo" = sol.producto) LEFT JOIN public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id")  LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") LEFT JOIN public.solicitud_usuarios usu2 ON (usu2.id = sol."usuarioResponsableCompra_id")  INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) INNER JOIN public.solicitud_estadosAlmacen est1 ON (est1.id = sol."estadosAlmacen_id") INNER JOIN public.solicitud_estadosvalidacion est2 ON (est2.id = "estadosCompras_id") inner join public.solicitud_areas areas on (areas.id = sol0.area_id) inner join public.solicitud_usuarios usuariosCreaSol on (usuariosCreaSol.id = sol0.usuarios_id) WHERE sol0.estadoReg = ' + "'A'" + ' AND sol. "estadosCompras_id" != 2 ORDER BY sol.item'

    cur.execute(comando)
    print(comando)

    solicitudDetalle = []
    #solicitudDetalle.append({"model":"solicitud.solicitudesdetalle"})

    if (perfil == 'C'):
      for solicitudNo,fecha,area,nombre_area,idUsuarioCreaSol,usuariosCreaSol, id, item, descripcion_id, descripcion, tipo, producto, nombre_producto, presentacion, cantidad, justificacion, tec, usuResp, estValidacion, estadosAlmacen, estadosValidacion_id, especificacionesAlmacen, estadosAlmacen_id , usuAlmacen  ,observacionesCompras,estadosCompras_id, estadosCompras,usuCompras, adjuntoCompras  in cur.fetchall():
        solicitudDetalle.append(
            {"model":"solicitud.solicitudesdetalle","pk":id,"fields":
                {"solicitudNo": solicitudNo, "fecha": fecha, "area": area, "nombre_area": nombre_area, "idUsuarioCreaSol": idUsuarioCreaSol, "usuariosCreaSol": usuariosCreaSol,
             "id": id, "item": item, "'descripcion_id": descripcion_id, "descripcion": descripcion, "tiposCompra": tipo,
             "producto": producto,"nombre_producto": nombre_producto,
             "presentacion": presentacion, "cantidad": cantidad, "justificacion": justificacion, "especificacionesTecnicas": tec,
             "usuarioResponsableValidacion": usuResp, "estadosValidacion": estValidacion,
             "estadosAlmacen": estadosAlmacen,
             "estadosValidacion_id": estadosValidacion_id,
             "especificacionesAlmacen":especificacionesAlmacen  , "estadosAlmacen_id":estadosAlmacen_id, "usuAlmacen":usuAlmacen,
             "observacionesCompras":observacionesCompras, "estadosCompras_id":estadosCompras_id,
             "estadosCompras":estadosCompras, "usuCompras":usuCompras, "adjuntoCompras":adjuntoCompras


             }})

    miConexion.close()
    print("solicitudDetalle")
    print(solicitudDetalle)

    # Cierro Conexion

    #{"model": "solicitud.solicitudesdetalle", "pk": 6, "fields":

    context['SolicitudDetalle'] = solicitudDetalle

    serialized1 = json.dumps(solicitudDetalle)

    print ("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')


def post_editCompras(request,id,username,sedeSeleccionada,nombreUsuario,nombreSede,perfil,solicitudId):
    print ("Entre POST edit compras")
    print ("id = " , id)

    print ("username =" , username)
    print("sedeSeleccionada =", sedeSeleccionada)
    print("nombreUsuario =", nombreUsuario)
    print("nombreSede =", nombreSede)
    print("solicitudId =", solicitudId)

    context = {}
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['solicitudId'] = solicitudId
    context['Perfil'] = perfil



    if request.method == 'GET':

        #solicitudesDetalle = SolicitudesDetalle.objects.filter(id=id).first()

        # Abro Conexion

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        # cur = miConexion.cursor()

        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        #comando = 'SELECT sol.id id ,sol.item item, sol.descripcion_id descripcion_id, des.nombre descripcion,sol."tiposCompra_id" tiposCompra_id, tip.nombre tipo , sol.producto producto, substring(art.articulo,1,150) nombre_producto ,sol.presentacion_id  presentacion_id, pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, sol."usuarioResponsableValidacion_id" usuarioResponsableValidacion_id,  usu.nom_usuario usuResp  , est.nombre estValidacion,est1.nombre estadosAlmacen  , sol."estadosValidacion_id" estadosValidacion_id ,  sol."especificacionesAlmacen" especificacionesAlmacen, sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen , sol."observacionesCompras" observacionesCompras, sol."estadosCompras_id" estadosCompras_id, est2.nombre estadosCompras, usu2.nom_usuario usuCompras     FROM public.solicitud_solicitudesDetalle sol , public.solicitud_descripcioncompra des, public.solicitud_tiposcompra tip, public.solicitud_presentacion pres, public.solicitud_articulos art    , public.solicitud_usuarios usu , public.solicitud_usuarios usu1 ,  public.solicitud_usuarios usu2 , public.solicitud_estadosvalidacion est, public.solicitud_estadosvalidacion est1, public.solicitud_estadosvalidacion est2 WHERE sol.id = ' + str(id) + ' AND des.id = sol.descripcion_id and tip.id = sol."tiposCompra_id" and pres.id = sol.presentacion_id and art."codregArticulo" = sol.producto and usu2.id = sol."usuarioResponsableCompra_id"  and usu1.id = sol."usuarioResponsableAlmacen_id" and usu.id = sol."usuarioResponsableValidacion_id" and est1.id = sol."estadosAlmacen_id"  and est2.id = sol."estadosCompras_id" and est.id = sol."estadosValidacion_id" ORDER BY sol.item'
        comando  = 'SELECT sol.id id, sol.item item, sol.descripcion_id descripcion_id, des.nombre descripcion,sol."tiposCompra_id" tiposCompra_id, tip.nombre tipo , sol.producto producto, substring(art.articulo,1,150) nombre_producto ,sol.presentacion_id  presentacion_id, pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec, sol."usuarioResponsableValidacion_id" usuarioResponsableValidacion_id,  usu.nom_usuario usuResp  , est.nombre estValidacion,est1.nombre estadosAlmacen  , sol."estadosValidacion_id" estadosValidacion_id ,  sol."especificacionesAlmacen" especificacionesAlmacen, sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen , sol."observacionesCompras" observacionesCompras, sol."estadosCompras_id" estadosCompras_id, est2.nombre estadosCompras, usu2.nom_usuario usuCompras, sol."adjuntoCompras"   adjuntoCompras   FROM public.solicitud_solicitudesDetalle sol INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id) INNER JOIN public.solicitud_articulos art   ON (art."codregArticulo" = sol.producto) LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") LEFT JOIN public.solicitud_usuarios usu2 ON (usu2.id = sol."usuarioResponsableCompra_id") INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) INNER JOIN public.solicitud_estadosvalidacion est1  ON (est1.id = sol."estadosAlmacen_id")  INNER JOIN public.solicitud_estadosvalidacion est2  ON (est2.id = "estadosCompras_id") WHERE sol.id = ' +  str(id) + ' ORDER BY sol.item '
        cur.execute(comando)
        print(comando)

        solicitudDetalle = []
        # solicitudDetalle.append({"model":"solicitud.solicitudesdetalle"})

        for id, item, descripcion_id, descripcion, tiposCompra_id, tipo, producto,nombre_producto, presentacion_id , presentacion, cantidad, justificacion, tec,usuarioResponsableValidacion_id, usuResp, estValidacion,estadosAlmacen, estadosValidacion_id, especificacionesAlmacen, estadosAlmacen_id , usuAlmacen   ,observacionesCompras,estadosCompras_id, estadosCompras,usuCompras,adjuntoCompras   in cur.fetchall():

            solicitudDetalle.append(
                {
                    #"model": "solicitud.solicitudesdetalle", "pk": id, "fields": {
                     "id": id, "item": item, "descripcion_id": descripcion_id, "descripcion": descripcion,
                    "tiposCompra_id": tiposCompra_id, "tiposCompra": tipo,
                     "producto": producto,"nombre_producto": nombre_producto,
                    "presentacion_id": presentacion_id,
                     "presentacion": presentacion, "cantidad": cantidad, "justificacion": justificacion,
                     "especificacionesTecnicas": tec,
                    "usuarioResponsableValidacion_id": usuarioResponsableValidacion_id,
                     "usuarioResponsableValidacion": usuResp, "estadosValidacion": estValidacion,
                     "estadosAlmacen": estadosAlmacen,
                     "estadosValidacion_id": estadosValidacion_id,
                    "especificacionesAlmacen":especificacionesAlmacen, "estadosAlmacen_id":estadosAlmacen_id,
                    "usuAlmacen":usuAlmacen,
                    "observacionesCompras": observacionesCompras, "estadosCompras_id": estadosCompras_id,
                    "estadosCompras": estadosCompras, "usuCompras": usuCompras, "adjuntoCompras":adjuntoCompras


                })

        miConexion.close()
        print("solicitudDetalle")
        print(solicitudDetalle)

        # Cierro Conexion


        print ("Me devuelvo a la MODAL")

        return JsonResponse({'pk':solicitudDetalle[0]['id'],'item':solicitudDetalle[0]['item'],
                             'descripcion_id': solicitudDetalle[0]['descripcion_id'],
                             'descripcion':solicitudDetalle[0]['descripcion'],'tiposCompra_id':solicitudDetalle[0]['tiposCompra_id'], 'tiposCompra':solicitudDetalle[0]['tiposCompra'],
                             'producto':solicitudDetalle[0]['producto'],
                             'nombre_producto': solicitudDetalle[0]['nombre_producto'],
                             'presentacion_id': solicitudDetalle[0]['presentacion_id'],
                             'presentacion':solicitudDetalle[0]['presentacion'],
                             'cantidad':solicitudDetalle[0]['cantidad'],'justificacion':solicitudDetalle[0]['justificacion'],
                             'especificacionesTecnicas':solicitudDetalle[0]['especificacionesTecnicas'],
                             'usuarioResponsableValidacion_id': solicitudDetalle[0]['usuarioResponsableValidacion_id'],
                             'usuarioResponsableValidacion':solicitudDetalle[0]['usuarioResponsableValidacion'],
                             'estadosValidacion':solicitudDetalle[0]['estadosValidacion'],
                             'estadosAlmacen': solicitudDetalle[0]['estadosAlmacen'],
                             'estadosValidacion_id': solicitudDetalle[0]['estadosValidacion_id'],
                             'especificacionesAlmacen':solicitudDetalle[0]['especificacionesAlmacen'],
                             'estadosAlmacen_id': solicitudDetalle[0]['estadosAlmacen_id'],
                             'usuAlmacen': solicitudDetalle[0]['usuAlmacen'],
                             'observacionesCompras': solicitudDetalle[0]['observacionesCompras'],
                             'estadosCompras_id': solicitudDetalle[0]['estadosCompras_id'],
                             'estadosCompras': solicitudDetalle[0]['estadosCompras'],
                             'usuCompras': solicitudDetalle[0]['usuCompras'],

                             })
    else:
        return JsonResponse({'errors':'Something went wrong!'})

def post_deleteCompras(request,id):
    print ("Entre a borrar")
    solicitudesDetalle = SolicitudesDetalle.objects.get(id=id)
    solicitudesDetalle.delete()
    return HttpResponseRedirect(reverse('index'))


# Fin Create your views here. para Compras

# Create your views here. para Ordenes de Compras

def OrdenesCompraConsulta1(request , username, sedeSeleccionada, nombreUsuario, nombreSede, perfil):
    pass
    print ("Entre a consulta Ordenes de Compra1 solicitud");
    context = {}

    print("username = ", username)
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['solicitudesForm'] = solicitudesForm
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = "SELECT areas.id id ,areas.area  area FROM public.solicitud_areas areas, public.solicitud_sedesCompra sedes WHERE areas.estadoreg = 'A' and areas.sede_id = sedes.id and  sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"
    #Reemplazado
    #comando = "SELECT areas.codreg_area id ,areas.area  area FROM mae_areas areas, imhotep_sedes sedes WHERE areas.activo = 'S' and areas.sede = sedes.sede and sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"
    cur.execute(comando)
    print(comando)

    areas = []

    for id, area in cur.fetchall():
        areas.append({'id': id, 'area': area})

    miConexion.close()

    context['Areas'] = areas

    return render(request, "Reportes/OrdenesCompraConsulta.html", context)


#class PostStoreOrdenesCompra(TemplateView):
class PostStoreOrdenesCompra(CreateView):
    #form_class = ordenesCompraForm
    model = OrdenesCompra
    template_name = 'Reportes/OrdenesCompraTrae22.html'
    fields = ['fechaElab', 'fechaRevi', 'fechaApro', 'estadoOrden', 'elaboro', 'revizo', 'aprobo',
              'area', 'contacto', 'entregarEn', 'telefono', 'proveedor', 'opciones', 'valorBruto',
             'descuento','valorParcial','iva','valorTotal','observaciones','responsableCompra','entragaMercancia','recibeMercancia','aproboCompraStaff']

    #success_url = "/ordenesCompra/OrdenesCompraBusca/"
    success_url = "/ordenesCompra/OrdenesCompraBusca/"


    def get_initial(self):
        print(" Entre initial  de PostStoreOrdenesCompra = ", self.kwargs)
        pk = self.kwargs["pk"]

        # Leo la Solicitud
        print(" Entre initial pk = ", pk)

        ## Primero con el Id que llega busco ahora si la solicitud

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = "SELECT DISTINCT sol0.solicitud_id valor FROM public.solicitud_solicitudesdetalle sol0 WHERE sol0.id = " + pk
        print(comando)
        cur.execute(comando)
        print(comando)

        solicitudx = []

        for valor in cur.fetchall():
            solicitudx.append({'valor': valor})

        miConexion.close()
        print("solicitudx ")
        print(solicitudx)

        for dato in solicitudx:
            print(dato)
            print(dato['valor'])
            print(json.dumps(dato['valor']))
            solicitudId = json.dumps(dato['valor'])

        solicitudId = solicitudId.replace("[", "")
        solicitudId = solicitudId.replace("]", "")

        #context['SolicitudId '] = solicitudId
        print("solicitudId = ", solicitudId)

        ## Fin busco la SolicitudId

        # Traigo los datos para pasar los defaults en initial

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        #comando = 'SELECT id,nombre FROM public.solicitud_estadosValidacion est'
        comando = 'select sol.usuarios_id idSol, sol.usuarios_id usuSolicita,sol0."usuarioResponsableCompra_id" usuCompras, sol0."usuarioResponsableCompra_id" respCompras, areas.id area from solicitud_solicitudes sol inner join solicitud_solicitudesdetalle sol0 ON (sol0.solicitud_id = sol.id) inner join solicitud_areas areas on (areas.id = sol.area_id) inner join solicitud_usuarios usu on (usu.id = sol.usuarios_id) inner join solicitud_usuarios usu1 on (usu1.id = sol0."usuarioResponsableCompra_id") where sol.id = ' + str(solicitudId) + ' limit 1'
        cur.execute(comando)
        print(comando)

        ordenCompra = []

        for idSol, usuSolicita, usuCompras, respCompras,area   in cur.fetchall():
            ordenCompra.append({'idSol': idSol, 'usuSolicita': usuSolicita, 'usuCompras':usuCompras, 'respCompras':respCompras, 'area':area})

        miConexion.close()
        print("ordenCompra")
        print(ordenCompra)

        initial = super(PostStoreOrdenesCompra, self).get_initial()



        if ordenCompra != []:


            initial['elaboro'] = ordenCompra[0]['idSol']
            initial['revizo'] = ordenCompra[0]['usuCompras']
            initial['responsableCompra'] = ordenCompra[0]['usuCompras']
            initial['area'] = ordenCompra[0]['area']
            initial['valorBruto'] = 0
            initial['descuento'] = 0
            initial['valorParcial'] = 0
            initial['iva'] = 0.19
            initial['valorTotal'] = 0
            initial['valorParcial'] = initial['valorBruto'] - initial['descuento']
            initial['valorTotal'] = initial['valorParcial'] * initial['iva']



        ## Fin traigo valores extraidos de la solicitud

        return initial


    def form_valid(self, form):

        print ("Entre Forma valida y kwargs = ",self.kwargs )
        pk = self.kwargs["pk"]
        username = self.kwargs["username"]
        sedeSeleccionada = self.kwargs["sedeSeleccionada"]
        nombreUsuario = self.kwargs["nombreUsuario"]
        nombreSede = self.kwargs["nombreSede"]
        perfil = self.kwargs["perfil"]

        print("FormaValida Clean = ", form.cleaned_data)
        print("form fechaElab = ", form.cleaned_data['fechaElab'])
        instance = form.save()

        idCompra = OrdenesCompra.objects.last().id


        print("idCompra = " , idCompra)

        context = {}

        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = nombreUsuario
        context['NombreSede'] = nombreSede
        context['Perfil'] = perfil


        ## Primero con el Id que llega busco ahora si la solicitud

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = "SELECT DISTINCT sol0.solicitud_id valor FROM public.solicitud_solicitudesdetalle sol0 WHERE sol0.id = " + pk
        print(comando)
        cur.execute(comando)
        print(comando)

        solicitudx = []

        for valor in cur.fetchall():
            solicitudx.append({'valor': valor})

        miConexion.close()
        print("solicitudx ")
        print(solicitudx)

        for dato in solicitudx:
            print(dato)
            print(dato['valor'])
            print(json.dumps(dato['valor']))
            solicitudId = json.dumps(dato['valor'])

        solicitudId = solicitudId.replace("[", "")
        solicitudId = solicitudId.replace("]", "")

        #context['SolicitudId '] = solicitudId
        print("solicitudId = ", solicitudId)
        context['SolicitudId'] = solicitudId
        ## Fin busco la SolicitudId

        ## Comienza la rutina que crea el archivo Excel

        # Contamos
        valeQuerySet = SolicitudesDetalle.objects.filter(solicitud_id=solicitudId, estadosCompras_id=3)

        print("vale =", valeQuerySet.count())

        totalRegistros = valeQuerySet.count()

        print("totalRegistros =", totalRegistros)
        print("VYa guarde la OC")

        context['NoOrdenCompra'] = idCompra
        context['SolicitudId'] = 0
        context['success'] = True
        context['message'] = 'Orden de Compra No ' + str(idCompra) + ' Created Successfully!'
        ## Comienzo a preparar la impresion EXCEL  de la Orden de Compra
        print("Voy a abril execl")

        # my_wb = openpyxl.Workbook(encoding='ascii')
        my_wb = openpyxl.Workbook()
        print("Voy a abril execl1")
        my_sheet = my_wb.active
        print("Voy a abril execl2")
        fuente1 = Font(name='Century', bold=True, size=11, color='0a0a0a')
        print("Voy a abril execl3")
        fuente2 = Font(name='Century', bold=False, size=11, color='0a0a0a')
        print("Comienzo execl")
        b1 = my_sheet['B1']
        b1.value = "NIT 830.507.718-8"
        e1 = my_sheet['E1']
        e1.value = "FORMATO"
        e1.font = fuente1
        e3 = my_sheet['E3']
        e3.value = "APOYO FINANCIERO COMPRAS"
        e3.font = fuente1
        e5 = my_sheet['E5']
        e5.value = "ORDEN DE COMPRA : " + str(idCompra)

        e5.font = fuente1
        print("pase1")
        j1 = my_sheet['J1']
        j1.value = "Código: FOR-AFI-ORDEN DE COMPRA"
        j2 = my_sheet['J2']
        j2.value = "Versión 4"
        j3 = my_sheet['J3']
        j3.value = "Fecha de Elaboración :"
        l3 = my_sheet['L3']
        l3.value = str(form.cleaned_data['fechaElab'])
        l3 = my_sheet['L3']
        l3.value = str(form.cleaned_data['fechaElab'])
        j4 = my_sheet['J4']
        j4.value = "Fecha de Revision"
        l4 = my_sheet['L4']
        l4.value = str(form.cleaned_data['fechaRevi'])
        j5 = my_sheet['J5']
        j5.value = "Fecha de Aprobacion"
        l5 = my_sheet['L5']
        l5.value = str(form.cleaned_data['fechaApro'])
        j6 = my_sheet['J6']
        j6.value = "Pagina"
        j6.font = fuente1
        l6 = my_sheet['L6']
        l6.value = "ESTADO"
        l6.font = fuente1
        print("pase2")
        b7 = my_sheet['B7']
        b7.value = "ELABORO"
        b7.font = fuente1
        c7 = my_sheet['C7']
        c7.value = str(form.cleaned_data['elaboro'])
        c7.font = fuente2

        f7 = my_sheet['F7']
        f7.value = "REVIZO"
        f7.font = fuente1
        g7 = my_sheet['G7']
        g7.value = str(form.cleaned_data['revizo'])
        g7.font = fuente2

        j7 = my_sheet['J7']
        j7.value = "APROBO"
        j7.font = fuente1

        k7 = my_sheet['K7']
        k7.value = str(form.cleaned_data['aprobo'])
        k7.font = fuente2

        print("pase21")
        e9 = my_sheet['E9']
        e9.value = "DATOS ORDEN DE COMPRA"
        e9.font = fuente1
        b11 = my_sheet['B11']
        b11.value = "FECHA"
        b11.font = fuente2
        d11 = my_sheet['D11']
        d11.value = str(form.cleaned_data['fechaElab'])
        print("pase22")
        g11 = my_sheet['G11']
        g11.value = "AREA"
        g11.font = fuente2
        print("pase23")
        h11 = my_sheet['H11']
        h11.value = str(form.cleaned_data['area'])

        k11 = my_sheet['K11']
        k11.value = "# Cotizacion:"
        k11.font = fuente1
        l11 = my_sheet['L11']
        l11.value = "Pedido No:"
        l11.font = fuente1
        b12 = my_sheet['B12']
        b12.value = "CONTACTO"
        b12.font = fuente2
        print("pase24")
        d12 = my_sheet['D12']
        d12.value = str(form.cleaned_data['contacto'])
        g12 = my_sheet['G12']
        g12.value = "ENTREGAR EN"
        g12.font = fuente2
        h12 = my_sheet['H12']
        h12.value = str(form.cleaned_data['entregarEn'])
        b13 = my_sheet['B13']
        b13.value = "TELEFONO"
        b13.font = fuente2
        d13 = my_sheet['D13']
        d13.value = str(form.cleaned_data['telefono'])
        b14 = my_sheet['B14']
        b14.value = "          Horario de Recepcion :"
        b14.font = fuente1
        e14 = my_sheet['E14']
        e14.value = "martes y jueves: 7:30 am a 12 pm y de 2:00 pm a 4:00 pm "
        e14.font = fuente1
        e15 = my_sheet['E15']
        e15.value = "DATOS DEL PROVEEDOR"
        e15.font = fuente1

        ## Extraemos los datos del Proveedor

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()

        comando = "SELECT prov.proveedor nombre, prov.nit nit, prov.telefono telefono, translate(btrim(prov.direccion::text),'óÓáÁéÉíÍúÚñÑ'::text,'oOaAeEiIuUnN'::text)  direccion, prov.correo correo FROM public.solicitud_proveedores prov WHERE prov.proveedor = '" + str(
            form.cleaned_data['proveedor']) + "'"
        print(comando)
        print("pase26")
        cur.execute("set client_encoding='LATIN1';")
        cur.execute(comando)
        print(comando)

        prov = []

        for nombre, nit, telefono, direccion, correo in cur.fetchall():
            prov.append({'nombre': nombre, 'nit': nit, 'telefono': telefono, 'direccion': direccion, 'correo': correo})

        miConexion.close()
        print("prov")
        print(prov)

        for x in prov:
            print("X = ", x)
            jsonProv = x

        nombreProveedor = jsonProv['nombre']
        nitProveedor = jsonProv['nit']
        telefonoProveedor = jsonProv['telefono']
        direccionProveedor = jsonProv['direccion']
        correoProveedor = jsonProv['correo']

        print("nombre Proveedor = ", nombreProveedor)
        print("Nit Proveedor = ", nitProveedor)
        print("telefonoProveedor = ", telefonoProveedor)
        print("direccionProveedor = ", direccionProveedor)
        print("correoProveedor = ", correoProveedor)

        ### FIN DATOS DEL PROVEEDOR

        print("Pase 50")
        b16 = my_sheet['B16']
        b16.value = "RAZON SOCIAL"
        b16.font = fuente2
        d16 = my_sheet['D16']
        d16.value = str(nombreProveedor)
        h16 = my_sheet['H16']
        h16.value = "NIT"
        h16.font = fuente1
        print("Pase 51")
        i16 = my_sheet['I16']
        i16.value = str(nitProveedor)
        print("Pase 52")
        k16 = my_sheet['K16']
        k16.value = "TELEFONO:"
        k16.font = fuente1
        print("Pase 53")
        l16 = my_sheet['L16']
        l16.value = str(telefonoProveedor)
        b17 = my_sheet['B17']
        b17.value = "DIRECCION:"
        b17.font = fuente1
        d17 = my_sheet['D17']
        d17.value = str(direccionProveedor)
        print("Pase 54")
        h17 = my_sheet['H17']
        h17.value = "E-MAIL:"
        h17.font = fuente1
        i17 = my_sheet['I17']
        i17.value = str(correoProveedor)
        print("Pase 55")
        b18 = my_sheet['B18']
        b18.value = "ATENCION:"
        b18.font = fuente2
        e20 = my_sheet['E20']
        e20.value = "DETALLE DE LA COMPRA"
        e20.font = fuente1
        #k20 = my_sheet['K20']
        #k20.value = "VALOR BRUTO"
        #k20.font = fuente1
        b21 = my_sheet['B21']
        b21.value = "ITEM"
        b21.font = fuente1
        c21 = my_sheet['C21']
        c21.value = "DESCRIPCION REF"
        c21.font = fuente1
        f21 = my_sheet['F21']
        f21.value = "PRESENT."
        f21.font = fuente1
        g21 = my_sheet['G21']
        g21.value = "IVA"
        g21.font = fuente1
        h21 = my_sheet['H21']
        h21.value = "CANTIDAD"
        h21.font = fuente1
        h22 = my_sheet['H22']
        h22.value = "SOLICITADA"
        h22.font = fuente1
        i22 = my_sheet['I22']
        i22.value = "RECIBIDA"
        i22.font = fuente1
        j21 = my_sheet['J21']
        j21.value = "VALOR UNITARIO"
        j21.font = fuente1
        k21 = my_sheet['K21']
        k21.value = "VALOR TOTAL"
        k21.font = fuente1
        k22 = my_sheet['K22']
        k22.value = "SOLICITADA"
        k22.font = fuente1
        l22 = my_sheet['L22']
        l22.value = "RECIBIDA"
        l22.font = fuente1

        print("Armo pah archivo")

        # archivo='w:/PLATAFORMAS 2021/BACKUPS IMHOTEP/OC/OC_'  + str(idCompra) + '.xlsx'
        archivo = 'w:OC_' + str(idCompra) + '.xlsx'
        # archivo = 'C:/EntornosPython/comprasTable/comprasTable/Archivos/OC_' + str(idCompra) + '.xlsx'
        print("Archivo =", archivo)

        ## DESDE AQUI RUTINA ACTUALIZA ITEM EN SOLICITUD DETALLE
        # Imprimo en un for los valores de los items

        campoItem=1
        voy=23

        for reg in range(1, totalRegistros + 1):

            var1 = "item_" + str(campoItem)
            while True:
                # Código
                if var1 in self.request.POST:
                    break
                else:
                    campoItem = campoItem + 1
                    var1 = "item_" + str(campoItem)

            print("item = ", campoItem)
            var1 = "item_" + str(campoItem)
            var2 = "iva_" + str(campoItem)
            var3 = "solcan_" + str(campoItem)
            var4 = "reccan_" + str(campoItem)
            var5 = "unitario_" + str(campoItem)
            var6 = "solval_" + str(campoItem)
            var7 = "recval_" + str(campoItem)
            print("var2 IVA_ = ", var2)
            data1 = self.request.POST[var1]
            data2 = self.request.POST[var2]
            data3 = self.request.POST[var3]
            data4 = self.request.POST[var4]
            data5 = self.request.POST[var5]
            data6 = self.request.POST[var6]
            data7 = self.request.POST[var7]


            print("Registro Completo = ",
                  data1 + ' ' + data2 + ' ' + data3 + ' ' + data4 + ' ' + data5 + ' ' + data6 + ' ' + data7)


            ## Rutina Actualiza uno a una los items de la solicitud

            miConexiont = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432",
                                           user="postgres", password="BD_m3d1c4l")
            print("Me conecte")
            curt = miConexiont.cursor()
            print("Abri cursor")
            comando = 'UPDATE solicitud_solicitudesDetalle set iva = ' + str(data2) + ', "recibidoOrdenCantidad" = ' + str(data4) + ', "recibidoOrdenValor" =' + str(data7) + ',"solicitadoOrdenCantidad" = ' + str(data3) + ',"solicitadoOrdenValor" = ' + str(data6) + ',"valorUnitario" = ' + str(data5) + ', "ordenCompra_id" = ' + str(idCompra) + ' WHERE solicitud_id = ' + solicitudId + ' AND item = ' + str(data1)

            print(comando)
            print("voy a ejecutar comando")
            resultado = curt.execute(comando)
            print("resultado =", resultado)
            n = curt.rowcount
            print("Registros commit = ", n)

            miConexiont.commit()

            # Aqui leer presentacion y descripcion de cada item a imprimir

            miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432",
                                          user="postgres", password="BD_m3d1c4l")
            miConexion.set_client_encoding('LATIN1')
            cur = miConexion.cursor()

            comando = "SELECT pres.nombre presentacion, des.nombre descripcion FROM public.solicitud_solicitudesdetalle sol, public.solicitud_descripcioncompra des, public.solicitud_presentacion pres WHERE sol.solicitud_id = '" + str(solicitudId) + "'" + " AND sol.descripcion_id = des.id AND sol.presentacion_id = pres.id AND sol.item = " + str(campoItem)

            print(comando)
            print("pase2666")
            cur.execute("set client_encoding='LATIN1';")
            cur.execute(comando)
            print(comando)

            datosAdic = []

            for presentacion, descripcion in cur.fetchall():
                datosAdic.append({'presentacion': presentacion, 'descripcion': descripcion})

            miConexion.close()
            print("datosAdic")
            print(datosAdic)

            for x in datosAdic:
                print("X = ", x)
                jsonAdic = x

            presentacion = jsonAdic['presentacion']
            descripcion = jsonAdic['descripcion']



            ## Fin trae presentacion, descripcion

            llaveb = 'b' + str(voy)
            llaveb1 = 'B' + str(voy)
            llaveb = my_sheet[llaveb1]
            llaveb.value = str(data1)

            print("Pase 566")

            # b23 = my_sheet['B23']
            # b23.value = str(data1)
            llavec = 'c' + str(voy)
            llavec1 = 'C' + str(voy)
            llavec = my_sheet[llavec1]
            llavec.value = descripcion
            # c23 = my_sheet['C23']
            # c23.value = "AqUi descripcion"

            print("Pase 567")
            llavef = 'f' + str(voy)
            llavef1 = 'F' + str(voy)
            llavef = my_sheet[llavef1]
            llavef.value = presentacion
            # f23 = my_sheet['F23']
            # f23.value = "AqUi presentacion"
            llaveg = 'g' + str(voy)
            llaveg1 = 'G' + str(voy)
            llaveg = my_sheet[llaveg1]
            llaveg.value = str(data2)

            print("Pase 568")
            # g23 = my_sheet['G23']
            # g23.value = str(data2)
            llaveh = 'h' + str(voy)
            llaveh1 = 'H' + str(voy)
            llaveh = my_sheet[llaveh1]
            llaveh.value = str(data3)
            # h23 = my_sheet['H23']
            # h23.value = str(data3)
            llavei = 'i' + str(voy)
            llavei1 = 'I' + str(voy)
            llavei = my_sheet[llavei1]
            llavei.value = str(data4)
            # i23 = my_sheet['I23']
            # i23.value = str(data4)
            print("Pase 569")
            llavej = 'j' + str(voy)
            llavej1 = 'J' + str(voy)
            llavej = my_sheet[llavej1]
            llavej.value = str(data5)
            # j23 = my_sheet['J23']
            # j23.value = str(data5)
            llavek = 'k' + str(voy)
            llavek1 = 'K' + str(voy)
            llavek = my_sheet[llavek1]
            llavek.value = str(data6)
            # k23 = my_sheet['K23']
            # k23.value = str(data6)
            print ("Pase 570")
            llavel = 'l' + str(voy)
            llavel1 = 'L' + str(voy)
            llavel = my_sheet[llavel1]
            llavel.value = str(data7)
            # l23 = my_sheet['L23']
            # l23.value = str(data7)
            print("Pase 571")
            voy = voy + 1

            ## Fin detalle Excel

            campoItem = campoItem + 1

        # seguimos con la ultima parte del archivo excel

        voy = voy + 2
        print("Pase 56")

        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value = "FORMA DE PAGO"
        llaveb.font = fuente1
        #b27 = my_sheet['B27']
        #b27.value = "FORMA DE PAGO"
        #b27.font = fuente1
        llaveh = 'h' + str(voy)
        llaveh1 = 'H' + str(voy)
        llaveh = my_sheet[llaveh1]
        llaveh.value = "VALOR BRUTO"
        llaveh.font = fuente1
        #h27 = my_sheet['H27']
        #h27.value = "VALOR BRUTO"
        #h27.font = fuente1
        llavel = 'l' + str(voy)
        llavel1 = 'L' + str(voy)
        llavel = my_sheet[llavel1]
        llavel.value = str(form.cleaned_data['valorBruto'])
        print("Pase 57")
        #l27 = my_sheet['L27']
        #l27.value = str(form.cleaned_data['valorBruto'])

        voy = voy + 1

        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value = "OPCION 1"
        llaveb.font = fuente1
        #b28 = my_sheet['B28']
        #b28.value = "OPCION 1"
        #b28.font = fuente1
        llavec = 'c' + str(voy)
        llavec1 = 'C' + str(voy)
        llavec = my_sheet[llavec1]
        llavec.value = "CONTRA ENTREGA"
        llavec.font = fuente2
        #c28 = my_sheet['C28']
        #c28.value = "CONTRA ENTREGA"
        #c28.font = fuente2
        llaveh = 'h' + str(voy)
        llaveh1 = 'H' + str(voy)
        llaveh = my_sheet[llaveh1]
        llaveh.value = "DESCUENTO %"
        llaveh.font = fuente1
        #h28 = my_sheet['H28']
        #h28.value = "DESCUENTO %"
        #h28.font = fuente1
        llavel = 'l' + str(voy)
        llavel1 = 'L' + str(voy)
        llavel = my_sheet[llavel1]
        llavel.value = str(form.cleaned_data['descuento'])
        #l28 = my_sheet['L28']
        #l28.value = str(form.cleaned_data['descuento'])

        voy = voy + 1

        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value = "OPCION 2"
        llaveb.font = fuente1
        #b29 = my_sheet['B29']
        #b29.value = "OPCION 2"
        #b29.font = fuente1
        llavec = 'c' + str(voy)
        llavec1 = 'C' + str(voy)
        llavec = my_sheet[llavec1]
        llavec.value = "ANTICIPO"
        llavec.font = fuente2
        #c29 = my_sheet['C29']
        #c29.value = "ANTICIPO"
        #c29.font = fuente2
        llavee = 'e' + str(voy)
        llavee1 = 'E' + str(voy)
        llavee = my_sheet[llavee1]
        llavee.value = "50 %"
        llavee.font = fuente2
        #e29 = my_sheet['E29']
        #e29.value = "50 %"
        #e29.font = fuente2
        llavef = 'f' + str(voy)
        llavef1 = 'F' + str(voy)
        llavef = my_sheet[llavef1]
        llavef.value = str(form.cleaned_data['opciones'])
        llavef.font = fuente2
        #f29 = my_sheet['F29']
        #f29.value = str(form.cleaned_data['opciones'])
        #f29.font = fuente2
        llaveh = 'h' + str(voy)
        llaveh1 = 'H' + str(voy)
        llaveh = my_sheet[llaveh1]
        llaveh.value = "VALOR PARCIAL"
        llaveh.font = fuente1
        #h29 = my_sheet['H29']
        #h29.value = "VALOR PARCIAL"
        #h29.font = fuente1
        llavel = 'l' + str(voy)
        llavel1 = 'L' + str(voy)
        llavel = my_sheet[llavel1]
        llavel.value = str(form.cleaned_data['valorParcial'])
        #l29 = my_sheet['L29']
        #l29.value = str(form.cleaned_data['valorParcial'])

        voy = voy + 1

        llavec = 'c' + str(voy)
        llavec1 = 'C' + str(voy)
        llavec = my_sheet[llavec1]
        llavec.value = "CONTRA ENTREGA"
        llavec.font = fuente2
        #c30 = my_sheet['C30']
        #c30.value = "CONTRA ENTREGA"
        #c30.font = fuente2
        llavee = 'e' + str(voy)
        llavee1 = 'E' + str(voy)
        llavee = my_sheet[llavee1]
        llavee.value = "50 %"
        llavee.font = fuente2
        #e30 = my_sheet['E30']
        #e30.value = "50 %"
        #e30.font = fuente2
        llaveh = 'h' + str(voy)
        llaveh1 = 'H' + str(voy)
        llaveh = my_sheet[llaveh1]
        llaveh.value = "IVA"
        llaveh.font = fuente1
        #h30 = my_sheet['H30']
        #h30.value = "IVA"
        #h30.font = fuente1
        llavel = 'l' + str(voy)
        llavel1 = 'L' + str(voy)
        llavel = my_sheet[llavel1]
        llavel.value = str(form.cleaned_data['iva'])
        #l30 = my_sheet['L30']
        #l30.value = str(form.cleaned_data['iva'])

        voy = voy + 1

        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value =  "OPCION 3"
        llaveb.font = fuente1
        #b31 = my_sheet['B31']
        #b31.value = "OPCION 3"
        #b31.font = fuente1
        llavec = 'c' + str(voy)
        llavec1 = 'C' + str(voy)
        llavec = my_sheet[llavec1]
        llavec.value =  "NOVENTA (90) DIAS"
        llavec.font = fuente2
        #c31 = my_sheet['C31']
        #c31.value = "NOVENTA (90) DIAS"
        #c31.font = fuente2
        print("Pase 58")
        voy = voy + 1

        llaveh = 'h' + str(voy)
        llaveh1 = 'H' + str(voy)
        llaveh = my_sheet[llaveh1]
        llaveh.value = "VALOR TOTAL"
        llaveh.font = fuente1
        #h31 = my_sheet['H31']
        #h31.value = "VALOR TOTAL"
        #h31.font = fuente1
        llavel = 'l' + str(voy)
        llavel1 = 'L' + str(voy)
        llavel = my_sheet[llavel1]
        llavel.value = form.cleaned_data['valorTotal']
        voy = voy + 1
        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value = "OPCION 4"
        llaveb.font = fuente1
        #b32 = my_sheet['B32']
        #b32.value = "OPCION 4"
        #b32.font = fuente1
        llaveh = 'h' + str(voy)
        llaveh1 = 'H' + str(voy)
        llaveh = my_sheet[llaveh1]
        llaveh.value = "OBSERVACIONES"
        llaveh.font = fuente1
        #h32 = my_sheet['H32']
        #h32.value = "OBSERVACIONES"
        #h32.font = fuente1

        llavel = 'l' + str(voy)
        llavel1 = 'L' + str(voy)
        llavel = my_sheet[llavel1]
        llavel.value =  str(form.cleaned_data['observaciones'])
        #l32 = my_sheet['L32']
        #l32.value = str(form.cleaned_data['observaciones'])

        voy = voy + 4

        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value = "RESPONSABLE ORDEN DE COMPRA:"
        llaveb.font = fuente1
        #b36 = my_sheet['B36']
        #b36.value = "RESPONSABLE ORDEN DE COMPRA:"
        #b36.font = fuente1
        llaveg = 'g' + str(voy)
        llaveg1 = 'G' + str(voy)
        llaveg = my_sheet[llaveg1]
        llaveg.value =  "QUIEN ENTREGA MERCANCIA:"
        llaveg.font = fuente1
        print("Pase 59")
        #g36 = my_sheet['G36']
        #g36.value = "QUIEN ENTREGA MERCANCIA:"
        #g36.font = fuente1
        llavek = 'k' + str(voy)
        llavek1 = 'K' + str(voy)
        llavek = my_sheet[llavek1]
        llavek.value = "QUIEN RECIBE MERCANCIA:"
        llavek.font = fuente1
        #k36 = my_sheet['K36']
        #k36.value = "QUIEN RECIBE MERCANCIA:"
        #k36.font = fuente1

        voy = voy + 2

        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value = str(form.cleaned_data['responsableCompra'])
        #b38 = my_sheet['B38']
        #b38.value = str(form.cleaned_data['responsableCompra'])
        print("Pase 60")
        llaveg = 'g' + str(voy)
        llaveg1 = 'G' + str(voy)
        llaveg = my_sheet[llaveg1]
        llaveg.value = str(form.cleaned_data['entragaMercancia'])
        #g38 = my_sheet['G38']
        #g38.value = str(form.cleaned_data['entragaMercancia'])
        llavek = 'k' + str(voy)
        llavek1 = 'K' + str(voy)
        llavek = my_sheet[llavek1]
        llavek.value = str(form.cleaned_data['recibeMercancia'])
        #k38 = my_sheet['K38']
        #k38.value = str(form.cleaned_data['recibeMercancia'])

        voy = voy + 5

        print("Pase 61")

        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value = "FIRMA Y SELLO"
        llaveb.font = fuente2
        #b43 = my_sheet['B43']
        #b43.value = "FIRMA Y SELLO"
        #b43.font = fuente2
        llaveg = 'g' + str(voy)
        llaveg1 = 'G' + str(voy)
        llaveg = my_sheet[llaveg1]
        llaveg.value = "FIRMA Y SELLO"
        llaveg.font = fuente2
        #g43 = my_sheet['G43']
        #g43.value = "FIRMA Y SELLO"
        #g43.font = fuente2
        llavek = 'k' + str(voy)
        llavek1 = 'K' + str(voy)
        llavek = my_sheet[llavek1]
        llavek.value = "FIRMA Y SELLO"
        llavek.font = fuente2
        #k43 = my_sheet['K43']
        #k43.value = "FIRMA Y SELLO"
        #k43.font = fuente2

        voy = voy + 1

        llaveb = 'b' + str(voy)
        llaveb1 = 'B' + str(voy)
        llaveb = my_sheet[llaveb1]
        llaveb.value = "NOTA ACLARATORIA. "
        llaveb.font = fuente1
        #b44 = my_sheet['B44']
        #b44.value = "NOTA ACLARATORIA. "
        #b44.font = fuente1

        llavee = 'e' + str(voy)
        llavee1 = 'E' + str(voy)
        llavee = my_sheet[llavee1]
        llavee.value = "TODA CANTIDAD RECIBIDA, MAYOR A LA SOLICITADA EN LA ORDEN DE COMPRA NO SERÁ PAGADA POR LA CLÍNICA MEDICAL S.A.S"
        llavee.font = fuente1

        #e44 = my_sheet['E44']
        #e44.value = "TODA CANTIDAD RECIBIDA, MAYOR A LA SOLICITADA EN LA ORDEN DE COMPRA NO SERÁ PAGADA POR LA CLÍNICA MEDICAL S.A.S"
        #e44.font = fuente2
        print("Pase Final")

        response = HttpResponse(content_type="application/ms-excel")
        contenido = "attachment; filename = {0}".format(archivo)
        response["Content-Disposition"] = contenido
        my_wb.save(archivo)
        # my_wb.save(response)
        # return response

        ## fin excel


        # Fin rutina que crea el archivo excel

        #return render(self.request, self.template_name, context)
        return render(self.request, "Reportes/cabeza.html", context)

    def get_context_data(self, **kwargs):
        print("GET_CONTEXT DEL VIEW DE POSTSTORE-ORDENES DE COMPRA con ANTES kwars = ", self.kwargs)
        context = super(PostStoreOrdenesCompra, self).get_context_data(**kwargs)
        print("GET_CONTEXT DEL VIEW DE ORDENES DE COMPRA con kwars = ", self.kwargs)

        # Create any data and add it to the context
        context['Aprobo'] = 'ALBERTO BERNAL'
        context['entregarEn'] = "JEISON MOLINA"

        pk = self.kwargs["pk"]
        username = self.kwargs["username"]
        sedeSeleccionada = self.kwargs["sedeSeleccionada"]
        nombreUsuario = self.kwargs["nombreUsuario"]
        nombreSede = self.kwargs["nombreSede"]
        perfil = self.kwargs["perfil"]

        print("pk =", pk)
        print("username =", username)
        print("sedeSeleccionada =", sedeSeleccionada)
        print("nombreUsuario =", nombreUsuario)
        print("nombreSede =", nombreSede)
        print("perfil =", perfil)

        #context = super().get_context_data(**kwargs)

        context['Username'] = username
        context['SedeSeleccionada'] = sedeSeleccionada
        context['NombreUsuario'] = nombreUsuario
        context['NombreSede'] = nombreSede
        context['Perfil'] = perfil
        #context['SolicitudId'] = solicitudId
        context['ordenesCompraForm'] = ordenesCompraForm

        #DESDE AQUIP

        # Buscamos estadosValidacion

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosValidacion est'
        cur.execute(comando)
        print(comando)

        estadosValidacion = []

        for id, nombre in cur.fetchall():
            estadosValidacion.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosValidacion")
        print(estadosValidacion)

        context['EstadosValidacion'] = estadosValidacion

        # Fin buscamos estdos validacion

        # Buscamos estadosAlmacen

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosAlmacen est'
        cur.execute(comando)
        print(comando)

        estadosAlmacen = []

        for id, nombre in cur.fetchall():
            estadosAlmacen.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosAlmacen")
        print(estadosAlmacen)

        context['EstadosAlmacen'] = estadosAlmacen

        # Fin buscamos estados Almacen

        # Buscamos estadosCompras

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = 'SELECT id,nombre FROM public.solicitud_estadosValidacion est'
        cur.execute(comando)
        print(comando)

        estadosCompras = []

        for id, nombre in cur.fetchall():
            estadosCompras.append({'id': id, 'nombre': nombre})

        miConexion.close()
        print("estadosCompras")
        print(estadosCompras)

        context['EstadosCompras'] = estadosCompras

        # Fin buscamos estados Almacen

        ## Primero con el Id que llega busco ahora si la solicitud

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()

        comando = "SELECT DISTINCT sol0.solicitud_id valor FROM public.solicitud_solicitudesdetalle sol0 WHERE sol0.id = " + pk
        print(comando)
        cur.execute(comando)
        print(comando)

        solicitudx = []

        for valor in cur.fetchall():
            solicitudx.append({'valor': valor})

        miConexion.close()
        print("solicitudx ")
        print(solicitudx)

        for dato in solicitudx:
                print(dato)
                print(dato['valor'])
                print(json.dumps(dato['valor']))
                solicitudId = json.dumps(dato['valor'])

        solicitudId = solicitudId.replace("[","")
        solicitudId = solicitudId.replace("]", "")

        context['SolicitudId '] = solicitudId
        print("solicitudId = ",solicitudId)


        ## Fin busco la SolicitudId

        # Buscamos la solicitud

        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        cur = miConexion.cursor()
        # Pendiente de reemplazo
        comando = "SELECT sol.id id, to_char(sol.fecha, 'YYYY-MM-DD HH:MM.SS')  fecha, sol.estadoReg estadoReg,sol.usuarios_id usuarioId , usu.nom_usuario nom_usuario, area.area nom_area, sede.nom_sede  nom_sede FROM public.solicitud_solicitudes sol ,public.solicitud_areas area , public.solicitud_sedesCompra sede, public.solicitud_usuarios usu WHERE sol.id = " + solicitudId + " AND area.id = sol.area_id and area.sede_id = sede.id and sol.usuarios_id = usu.id"
        cur.execute(comando)
        print(comando)

        solicitud = []

        for id, fecha, estadoReg, usuarioId, nom_usuario, nom_area, nom_sede in cur.fetchall():
            solicitud.append(
                {'id': id, 'fecha': fecha, 'estadoReg': estadoReg, 'usuarioId': usuarioId, 'nom_usuario': nom_usuario,
                 'nom_area': nom_area, 'nom_sede': nom_sede})

        miConexion.close()
        print("solicitud")
        print(solicitud)

        context['Solicitud'] = solicitud

        # Ahora SolicitudDetalle
        # Fin SolicitudDetalle
        if (solicitud == []):
            print("Entre por No existe")
            context['Error'] = 'Solicitud No Existe '
            miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                          password="BD_m3d1c4l")

            miConexion.set_client_encoding('LATIN1')
            cur = miConexion.cursor()
            cur.execute("set client_encoding='LATIN1';")
            comando = "SELECT areas.id id ,areas.area  area FROM public.solicitud_areas areas, public.solicitud_sedesCompra sedes WHERE areas.estadoreg = 'A' and areas.sede_id = sedes.id and  sedes.codreg_sede = '" + sedeSeleccionada + "' order by areas.area"
            cur.execute(comando)
            print(comando)
            areas = []
            areas.append({'id': '', 'area': ''})

            for id, area in cur.fetchall():
                areas.append({'id': id, 'area': area})

            miConexion.close()

            context['Areas'] = areas

            print ("No encontre data")

            #return HttpResponse(context, content_type='application/json')
            #return JsonResponse(context)
            #return render(self.request, "Reportes/ValidacionConsulta.html", {'ERROR':'Solicitud No Existe'})
            return context
        else:
            # POr aqui si existe
            ## Desde aquip codigo para la vista de ordenescompratrae2

            # Abro Conexion

            miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                          password="BD_m3d1c4l")
            # cur = miConexion.cursor()

            miConexion.set_client_encoding('LATIN1')
            cur = miConexion.cursor()
            cur.execute("set client_encoding='LATIN1';")


            #comando = 'SELECT sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion, sol."solicitadoAlmacen" solicitadoAlmacen,sol.iva iva ,sol."recibidoOrdenCantidad" recibidoOrdenCantidad,sol."recibidoOrdenValor" recibidoOrdenValor,sol."solicitadoOrdenCantidad" solicitadoOrdenCantidad,sol."solicitadoOrdenValor" solicitadoOrdenValor,sol."valorUnitario" valorUnitario FROM public.solicitud_solicitudesDetalle sol , public.solicitud_descripcioncompra des, public.solicitud_tiposcompra tip, public.solicitud_presentacion pres, public.solicitud_articulos art    , public.solicitud_usuarios usu , public.solicitud_usuarios usu1 , public.solicitud_usuarios usu2,  public.solicitud_estadosvalidacion est , public.solicitud_estadosvalidacion est1 , public.solicitud_estadosvalidacion est2  WHERE sol.solicitud_id = ' + solicitudId + ' AND est2.nombre like (' + "'" + '%APROBA%' + "'" + ')  AND  (sol."ordenCompra_id"= 0 OR  sol."ordenCompra_id" is null)  AND des.id = sol.descripcion_id and tip.id = sol."tiposCompra_id" and pres.id = sol.presentacion_id and art."codregArticulo" = sol.producto and  usu2.id = sol."usuarioResponsableCompra_id"   and usu1.id = sol."usuarioResponsableAlmacen_id" and usu.id = sol."usuarioResponsableValidacion_id" and est1.id = sol."estadosAlmacen_id" and est2.id = "estadosCompras_id"  and est.id = sol."estadosValidacion_id" ORDER BY sol.item'
            comando = 'SELECT sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion, sol."solicitadoAlmacen" solicitadoAlmacen,sol.iva iva ,sol."recibidoOrdenCantidad" recibidoOrdenCantidad,sol."recibidoOrdenValor" recibidoOrdenValor,sol."solicitadoOrdenCantidad" solicitadoOrdenCantidad,sol."solicitadoOrdenValor" solicitadoOrdenValor,sol."valorUnitario" valorUnitario , "adjuntoCompras" adjuntoCompras FROM public.solicitud_solicitudesDetalle sol INNER JOIN  public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id) INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id") INNER JOIN public.solicitud_presentacion pres ON (pres.id = sol.presentacion_id) INNER JOIN public.solicitud_articulos art   ON (art."codregArticulo" = sol.producto) LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id" ) LEFT JOIN public.solicitud_usuarios usu2 ON (usu2.id = sol."usuarioResponsableCompra_id" ) INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id") INNER JOIN public.solicitud_estadosvalidacion est1 ON (est1.id = sol."estadosAlmacen_id") INNER JOIN public.solicitud_estadosvalidacion est2  ON (est2.id = "estadosCompras_id") WHERE sol.solicitud_id = ' + solicitudId + ' AND est2.nombre like (' + "'" + '%APROBA%' + "'" + ')  AND  (sol."ordenCompra_id"= 0 OR  sol."ordenCompra_id" is null)  ORDER BY sol.item'
            cur.execute(comando)
            print(comando)

            solicitudDetalle = []
            # solicitudDetalle.append({"model":"solicitud.solicitudesdetalle"})

            for id, item, descripcion_id, descripcion, tipo, producto, nombre_producto, presentacion, solicitadoAlmacen, iva, recibidoOrdenCantidad, recibidoOrdenValor, solicitadoOrdenCantidad, solicitadoOrdenValor, valorUnitario , adjuntoCompras in cur.fetchall():
                solicitudDetalle.append(
                     {"id": id, "item": item, "descripcion": descripcion, "tiposCompra": tipo,
                         "producto": producto, "nombre_producto": nombre_producto,
                         "presentacion": presentacion,"solicitadoAlmacen":solicitadoAlmacen,
                      "iva": iva, "recibidoOrdenCantidad": recibidoOrdenCantidad,
                         "recibidoOrdenValor": recibidoOrdenValor, "solicitadoOrdenCantidad": solicitadoOrdenCantidad,
                         "solicitadoOrdenValor":solicitadoOrdenValor, "valorUnitario": valorUnitario, "adjuntoCompras":adjuntoCompras
                         })

            miConexion.close()
            print("solicitudDetalle")
            print(solicitudDetalle)

            # Cierro Conexion

            context['SolicitudDetalle'] = solicitudDetalle

            ## Fin

            return context

    def form_invalid(self, form):
            print("Entre form_invalid de OC pero no volvi ...")
            response = super().form_invalid(form)
            print("pase1")
            print("responde = ", response)
            if self.request.accepts('text/html'):
                print("pase2")

                return response
            else:
                print("pase3")
                return JsonResponse(form.errors, status=400)

        #HASTA AQUIP class PostStoreCompras

def load_dataOrdenesCompra(request, solicitudId):
    print ("Entre load_data Ordenes de Compras")
    print("solicitudId = ",solicitudId)

    #print("data = ", request.GET('data'))

    solicitudesDetalleList = SolicitudesDetalle.objects.all().filter(solicitud_id=solicitudId)

    # Ahora SolicitudDetalle
    context= {}

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    # cur = miConexion.cursor()

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")


    #comando =  'SELECT sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,usu.nom_usuario usuResp  , est.nombre estValidacion,est1.nombre estadosAlmacen, sol."estadosValidacion_id" estadosValidacion_id, sol."especificacionesAlmacen" especificacionesAlmacen, sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen FROM public.solicitud_solicitudesDetalle sol , public.solicitud_descripcioncompra des, public.solicitud_tiposcompra tip, public.solicitud_presentacion pres, public.solicitud_articulos art    , public.solicitud_usuarios usu , public.solicitud_usuarios usu1 , public.solicitud_estadosvalidacion est , public.solicitud_estadosvalidacion est1  WHERE sol.solicitud_id = ' + solicitudId + ' AND des.id = sol.descripcion_id and tip.id = sol."tiposCompra_id" and pres.id = sol.presentacion_id and art."codregArticulo" = sol.producto and usu1.id = sol."usuarioResponsableAlmacen_id" and usu.id = sol."usuarioResponsableValidacion_id" and est1.id = sol."estadosAlmacen_id" and est.id = sol."estadosValidacion_id" ORDER BY sol.item'
    #comando = 'SELECT sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion, sol.iva iva ,sol."recibidoOrdenCantidad" recibidoOrdenCantidad,sol."recibidoOrdenValor" recibidoOrdenValor,sol."solicitadoOrdenCantidad" solicitadoOrdenCantidad,sol."solicitadoOrdenValor" solicitadoOrdenValor,sol."valorUnitario" valorUnitario FROM public.solicitud_solicitudesDetalle sol , public.solicitud_descripcioncompra des, public.solicitud_tiposcompra tip, public.solicitud_presentacion pres, public.solicitud_articulos art    , public.solicitud_usuarios usu , public.solicitud_usuarios usu1 , public.solicitud_usuarios usu2,  public.solicitud_estadosvalidacion est , public.solicitud_estadosvalidacion est1 , public.solicitud_estadosvalidacion est2  WHERE sol.solicitud_id = ' + solicitudId + ' AND sol."estadosAlmacen_id" = 3  AND des.id = sol.descripcion_id and tip.id = sol."tiposCompra_id" and pres.id = sol.presentacion_id and art."codregArticulo" = sol.producto and  usu2.id = sol."usuarioResponsableCompra_id"   and usu1.id = sol."usuarioResponsableAlmacen_id" and usu.id = sol."usuarioResponsableValidacion_id" and est1.id = sol."estadosAlmacen_id" and est2.id = "estadosCompras_id"  and est.id = sol."estadosValidacion_id" ORDER BY sol.item'
    cur.execute(comando)
    print(comando)

    solicitudDetalle = []
    #solicitudDetalle.append({"model":"solicitud.solicitudesdetalle"})


    for id, item, descripcion_id, descripcion, tipo, producto, nombre_producto, presentacion, iva ,recibidoOrdenCantidad,recibidoOrdenValor,solicitadoOrdenCantidad,solicitadoOrdenValor,valorUnitario  in cur.fetchall():
        solicitudDetalle.append(
            {"model":"solicitud.solicitudesdetalle","pk":id,"fields":
            {"id": id, "item": item,  "descripcion": descripcion, "tiposCompra": tipo,
             "producto": producto,"nombre_producto": nombre_producto,
             "presentacion": presentacion, "iva":0, "recibidoOrdenCantidad":0,
             "recibidoOrdenValor" : 0,"solicitadoOrdenCantidad" : 0,
             "solicitadoOrdenValor" : 0, "valorUnitario" : 0
             }})

    miConexion.close()
    print("solicitudDetalle")
    print(solicitudDetalle)

    # Cierro Conexion

    #{"model": "solicitud.solicitudesdetalle", "pk": 6, "fields":

    context['SolicitudDetalle'] = solicitudDetalle

    serialized1 = json.dumps(solicitudDetalle)

    print ("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')

def descargaArchivo(request, archivo):

    print ("Entro A Descargar Archivo")

    nombreReporte = 'C:\EntornosPython\comprasTable\comprasTable\Archivos_OC_116'
    nombreReporteFinal = nombreReporte + ".xlsx"

    response = HttpResponse(content_type="application/ms-excel")
    #response.write(u'\ufeff'.encode('utf8'))
    contenido = "attachment; filename = {0}".format(nombreReporteFinal)
    #contenido = "attachment; filename = " + nombreReporteFinal
    response["Content-Disposition"] = contenido

    return response

def ReportesConsulta(request, username, sedeSeleccionada, nombreUsuario, nombreSede, perfil):

    context = {}
    print ("username = " , username )

    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil

    ## Consigo el listado de coordinadores

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = "SELECT id,nom_usuario  FROM public.solicitud_usuarios WHERE estadoReg = '" + "A' and perfil  = 'S' ORDER BY nom_usuario"
    cur.execute(comando)
    print(comando)

    coordinadores = []

    for id, nom_usuario in cur.fetchall():
        coordinadores.append({'id': id, 'nom_usuario': nom_usuario})



    context['Coordinadores'] = coordinadores

    print("coordinadores = ", coordinadores)

    miConexion.close()

    ## fin listado Coordinadores

    return render(request, 'Reportes\ReportesConsulta.html', context )

## aqui deb ir PostStoreReportesConsulta


## Fin de PostStoreReportesConsulta


## Desde Aqui Consulta Ordenes de Compras

def OrdenesCompraConsulta(request, username, sedeSeleccionada, nombreUsuario, nombreSede, perfil):

    context = {}
    print ("username = " , username )

    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil



    print ("Entre Consulta OrdenesCompra")


    return render(request, 'Reportes\OrdenesCompraConsulta1.html', context )


def load_dataOrdenesCompraConsulta(request, data):
    print("Entre DE VERDAD load_dataOrdenesCompraConsulta ")

    #data = request.GET['data']
    print ("data = ", data)
    d = json.loads(data)
    desdeFechaSolicitud = d['desdeFechaSolicitud']
    hastaFechaSolicitud = d['hastaFechaSolicitud']

    username = d['username']
    nombreSede = d['nombreSede']
    nombreUsuario = d['nombreUsuario']
    sedeSeleccionada = d['sedeSeleccionada']
    solicitudId = d['solicitudId']
    perfil = d['perfil']

    print("desdeFechaSolicitud = ", d['desdeFechaSolicitud'])
    print("hastaFechaSolicitud = ", d['hastaFechaSolicitud'])
    print("voy a context0")
    # Ahora SolicitudDetalle
    print("voy a context1")
    context = {}
    print ("pase contex2")

    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada
    context['NombreUsuario'] = nombreUsuario
    context['NombreSede'] = nombreSede
    context['Perfil'] = perfil
    context['solicitudId'] = solicitudId
    context['desdeFechaSolicitud'] = desdeFechaSolicitud
    context['hastaFechaSolicitud'] = hastaFechaSolicitud

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres", password="BD_m3d1c4l")
    # cur = miConexion.cursor()

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")
    print("voy comando")
    #comando = 'select ord.id id, substring(to_char(ord."fechaElab",' + "'" +'yyyy-mm-dd' + "'" + '),1,10) fechaElab, ord."estadoOrden" estadoOrden ,ord.opciones opciones,ord."valorBruto" valorBruto,ord."descuento" descuento,ord."valorParcial" valorParcial, ord."iva" iva, ord."valorTotal" valorTotal,ord.observaciones observaciones,ord.area_id area, ord.proveedor_id proveedor,sol.item item,art.articulo, sol.iva iva,sol."recibidoOrdenCantidad" recibidoOrdenCantidad,sol."solicitadoOrdenCantidad" solicitadoOrdenCantidad ,sol."valorUnitario" valorUnitario	, sol."solicitadoOrdenValor" solicitadoOrdenValor,sol."recibidoOrdenValor" recibidoOrdenValor FROM solicitud_ordenesCompra ord, solicitud_solicitudesdetalle sol, solicitud_articulos art WHERE ord."fechaElab" >= ' + "'" + desdeFechaSolicitud + "'" + ' and ord."fechaElab" <= ' + "'" +  hastaFechaSolicitud + "'" + ' and ord.id = sol."ordenCompra_id" and sol.producto = art."codregArticulo" ORDER BY ord."fechaElab", sol.item'
    comando = 'select ord.id id, substring(to_char(ord."fechaElab",' + "'" + 'yyyy-mm-dd' + "'" + '),1,10) fechaElab, ord."estadoOrden" estadoOrden ,ord.opciones opciones,ord."valorBruto" valorBruto,ord."descuento" descuento,ord."valorParcial" valorParcial, ord."iva" iva, ord."valorTotal" valorTotal,ord.observaciones observaciones,ord.area_id area, ord.proveedor_id proveedor,sol.item item,art.articulo, sol.iva iva,sol."recibidoOrdenCantidad" recibidoOrdenCantidad,sol."solicitadoOrdenCantidad" solicitadoOrdenCantidad ,sol."valorUnitario" valorUnitario	, sol."solicitadoOrdenValor" solicitadoOrdenValor,sol."recibidoOrdenValor" recibidoOrdenValor ,proveedor proveedor, area.area, usu.nom_usuario usuarioCompras,  usu1.nom_usuario usuarioAproboStaff FROM solicitud_ordenesCompra ord INNER JOIN solicitud_solicitudesdetalle sol ON (sol."ordenCompra_id" = ord.id) INNER JOIN solicitud_articulos art ON (art."codregArticulo" = sol.producto) INNER JOIN solicitud_proveedores prov on (prov.id = ord.proveedor_id) INNER JOIN solicitud_areas area on (area.id = ord.area_id) INNER JOIN solicitud_usuarios usu on (usu.id = ord."responsableCompra_id") INNER JOIN solicitud_Staff usu1 on (usu1.id = ord."aproboCompraStaff_id")  WHERE ord."fechaElab" >= ' + "'" + desdeFechaSolicitud + "'" + ' and ord."fechaElab" <= ' + "'" + hastaFechaSolicitud + "'" + ' and ord.id = sol."ordenCompra_id" and sol.producto = art."codregArticulo" ORDER BY ord."fechaElab", sol.item'

    print("pase comando")
    cur.execute(comando)
    print(comando)

    ordenCompra = []

    if (perfil == 'C'):

      for id, fechaElab, estadoOrden , opciones,valorBruto ,descuento, valorParcial,iva, valorTotal, observaciones,area,proveedor,item,articulo, iva,recibidoOrdenCantidad,solicitadoOrdenCantidad,valorUnitario,  solicitadoOrdenValor, recibidoOrdenValor ,proveedor, area, usuarioCompras, usuarioAproboStaff in cur.fetchall():
        ordenCompra.append(
            {"model": "solicitud.ordenescompra", "pk": id, "fields":
                {"id": id, "fechaElab":fechaElab, "estadoOrden": estadoOrden, "opciones": opciones, "valorBruto": valorBruto,
                  "valorParcial": valorParcial,"descuento":descuento,
                "iva": iva, "valorTotal": valorTotal, "observaciones": observaciones, "area": area, "proveedor": proveedor,
             "item": item, "articulo": articulo, "iva": iva,
             "recibidoOrdenCantidad": recibidoOrdenCantidad,"solicitadoOrdenCantidad": solicitadoOrdenCantidad ,
                 "valorUnitario":valorUnitario,"solicitadoOrdenValor":solicitadoOrdenValor , "recibidoOrdenValor": recibidoOrdenValor,
                 "proveedor":proveedor,"area":area, "usuarioCompras":usuarioCompras, "usuarioAproboStaff":usuarioAproboStaff}})

    miConexion.close()
    print("ordenCompra")
    print(ordenCompra)

    # Cierro Conexion

    context['OrdenCompra'] = ordenCompra

    ## Voy a enviar estadosSolicitudes

    serialized1 = json.dumps(ordenCompra , cls=DecimalEncoder)

    print("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')

class PostStoreOrdenesCompraConsulta(TemplateView):
        form_class = ordenesCompraForm
        template_name = 'Reportes/OrdenesCompraConsultaTrae1.html'

        def post(self, request):
            print("Entre a post de OrdenesCompraConsultas")

            context = {}

            return JsonResponse({'success': True, 'message': 'Orden Compra Created Successfully!'})

        def get_context_data(self, **kwargs):
            print("ENTRE POR EL GET_CONTEXT DEL VIEW de PostStoreOrdenesCOmpraConsulta : ")
            #solicitudId = self.request.GET["solicitudId"]

            username = self.request.GET['username']

            sedeSeleccionada = self.request.GET["sedeSeleccionada"]
            nombreUsuario = self.request.GET["nombreUsuario"]
            nombreSede = self.request.GET["nombreSede"]
            perfil = self.request.GET["perfil"]

            #print("SolictudId =", solicitudId)
            #print("username =", username)
            #print("sedeSeleccionada =", sedeSeleccionada)
            #print("nombreUsuario =", nombreUsuario)
            #print("nombreSede =", nombreSede)

            # context = super(PostStore, self).get_context_data(**kwargs)
            context = super().get_context_data(**kwargs)

            context['Username'] = username
            context['SedeSeleccionada'] = sedeSeleccionada
            context['NombreUsuario'] = nombreUsuario
            context['NombreSede'] = nombreSede
            context['Perfil'] = perfil
            #context['SolicitudId'] = solicitudId
            desdeFechaSolicitud = self.request.GET['desdeFechaSolicitud']
            hastaFechaSolicitud = self.request.GET['hastaFechaSolicitud']

            print("desdeFechaSolicitud = ", desdeFechaSolicitud)
            print("hastaFechaSolicitud = ", hastaFechaSolicitud)

            context['DesdeFechaSolicitud'] = desdeFechaSolicitud
            context['HastaFechaSolicitud'] = hastaFechaSolicitud

            return context


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)
## Fin Consilta Ordenes de Compras


def Simple_Upload(request, pk):
        print("Entre Ajax0 pk = ", pk)

    #if request.is_ajax():
        print ("Entre Ajax pk = ", pk)

          ## Consigie el archivo o ombre del archivo en la tabla ...
        # Abro Conexion


        miConexion = psycopg2.connect(host="192.168.0.237", database="bd_solicitudes2", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        comando = 'SELECT sol."adjuntoCompras" archivo FROM public.solicitud_solicitudesDetalle sol WHERE sol.id = ' + str(pk)
        cur.execute(comando)
        print(comando)

        archivos = []

        for archivo in cur.fetchall():
            archivos.append({"archivo": archivo})

        miConexion.close()
        print("archivos ")
        print(archivos)

        # Cierro Conexion

        for dato in archivos:
            print(dato)
            print(dato['archivo'])
            print(json.dumps(dato['archivo']))
            archivost = json.dumps(dato['archivo'])


        archivost = archivost.replace("(","")
        archivost = archivost.replace(")", "")
        archivost = archivost.replace("[", "")
        archivost = archivost.replace("]", "")
        archivost = archivost.replace(",", "")
        archivost = archivost.replace('"', "")
        #archivost = archivost.replace('/', "\\")
        archivost = archivost.replace('Uploaded Files/', "")

        filename = archivost

        print ("filename = ", filename)

        if (filename == ''):
            print ("Entre nO hay archivo")
            
            return HttpResponse ("no hay archivo")

        if (filename == "null"):

            print("Entre nO hay archivo")
            return HttpResponse("no hay archivo")
            #return HttpResponseRedirect(reverse('post_storeCompras'), {'Username': username, 'SedeSeleccionada': sedeSeleccionada, 'NombreUsuario': nombreUsuario, 'NombreSede': nombreSede, 'Perfil': perfil})
            #return redirect ('/ComprasConsulta')

        #filepath = BASE_DIR + 'C:\\EntornosPython\\comprasTable2\\comprasTable2\\media\\Uploaded Files' + filename
        #filepath = 'C:\\EntornosPython\\comprasTable2\\comprasTable2\\media\\uploaded Files\\' + filename
        filepath = 'C:\\EntornosPython\\comprasTable2\\comprasTable2\\media\\Uploaded Files\\' + filename
        print ("filepath", filepath)

        path = open(filepath, 'rb')

        print (" ya lei el archivo = ",filepath)

        mime_type = mimetypes.guess_type(filepath)

        print ("Voy de regreso")
        #response = HttpResponse(content_type="application/ms-excel")
        #response = HttpResponse(content_type='text/csv')

        response = HttpResponse(path, content_type=mime_type)

        response['Content-Disposition'] = f"attachment; filename={filename}"

        print("Chaolin")

        return response


