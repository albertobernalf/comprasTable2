
1013605270  coord cartera
1234


80760858  "JEISON MOLINA"   VALIDACION
1234


52973594   --CORELLY   COMPRAS
12345

79717519   --"EDWIN JAIR CUBIDES PIRAMANRIQUE"  ALMACEN
1234

select * from solicitud_usuarios;


select * from solicitud_usuarios WHERE NOM_USUARIO LIKE ('%MOLINA%');
select * from solicitud_solicitudes;	
select * from solicitud_estadosvalidacion;

 

select * from solicitud_proveedores where id= 7;
select * from solicitud_usuarios  where id in (11,21,18)
"Uploaded Files/Diccionario_Datos_imhotep_IGr16nW.xlsx"
select * from solicitud_ordenesCompra;
select * from solicitud_solicitudesdetalle where solicitud_id=21;
select * from solicitud_solicitudesdetalle where id=21;

update solicitud_solicitudesdetalle set "tipoAdjuntoCompras"='Csv' where id=26;
update solicitud_solicitudesdetalle set "estadosCompras_id"=1 where id=22;

update solicitud_solicitudesdetalle set "adjuntoCompras" = 'Diccionario_Datos_imhotep_IGr16nW.csv'  where  id=18;

update solicitud_solicitudesdetalle set "adjuntoCompras" = 'w:OC_28.XLSX' WHERE id=11;
update solicitud_solicitudesdetalle set "adjuntoCompras" = 'w:OC_28.XLSX' WHERE id=8;
select * from solicitud_solicitudes;
select * from solicitud_areas;
select * from solicitud_usuarios;
select * from solicitud_ordenesCompra;
1013605270






-- Validacion

SELECT sol0.id solicitudNo,to_char(sol0.fecha,'YYYY - MM - DD HH: MM.SS') fecha, sol0.area_id area, areas.area nombre_area, sol0.usuarios_id idUsuarioCreaSol , usuariosCreaSol.nom_usuario usuariosCreaSol, sol.id id, sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo, sol.producto producto, art.articulo nombre_producto, pres.nombre  presentacion, sol.cantidad, sol.justificacion, sol."especificacionesTecnicas" tec, usu.nom_usuario usuResp,  est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id
 FROM public.solicitud_solicitudes sol0 
inner join  public.solicitud_solicitudesDetalle sol on (sol.solicitud_id=sol0.id) 
inner join public.solicitud_descripcioncompra des on (des.id = sol.descripcion_id ) 
inner join public.solicitud_tiposcompra tip on (tip.id = sol."tiposCompra_id" ) 
inner join public.solicitud_presentacion pres on (pres.id = sol.presentacion_id ) 
inner join public.mae_articulos art on (art.codreg_articulo = sol.producto) 
left join public.solicitud_usuarios usu on (usu.id = sol."usuarioResponsableValidacion_id") 
inner join public.solicitud_estadosvalidacion est on (est.id = sol."estadosValidacion_id") 
inner join public.solicitud_areas areas on (areas.id = sol0.area_id) 
inner join public.solicitud_usuarios usuariosCreaSol on (usuariosCreaSol.id = sol0.usuarios_id) 
WHERE  sol0.estadoReg = 'A' AND sol."estadosValidacion_id" = 1 ORDER BY sol.item



-- Almacen

SELECT sol0.id solicitudNo,to_char(sol0.fecha,'YYYY - MM - DD HH: MM.SS') fecha, sol0.area_id area, areas.area nombre_area, sol0.usuarios_id idUsuarioCreaSol , usuariosCreaSol.nom_usuario usuariosCreaSol, 
sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,
pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,usu.nom_usuario usuResp  , est.nombre estValidacion, 
est1.nombre estadosAlmacen, sol."estadosValidacion_id" estadosValidacion_id, sol."especificacionesAlmacen" especificacionesAlmacen, 
sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen 
FROM public.solicitud_solicitudes sol0 
INNER JOIN public.solicitud_solicitudesDetalle sol on (sol.solicitud_id=sol0.id)
INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) 
INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) 
INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id) 
INNER JOIN public.mae_articulos art   ON (art.codreg_articulo = sol.producto) 
LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") 
LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") 
INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) 
INNER JOIN public.solicitud_estadosvalidacion est1  ON (est1.id = sol."estadosAlmacen_id") 
inner join public.solicitud_areas areas on (areas.id = sol0.area_id) 
inner join public.solicitud_usuarios usuariosCreaSol on (usuariosCreaSol.id = sol0.usuarios_id) 
WHERE  sol0.estadoReg = 'A' AND sol."estadosAlmacen_id" = 1
ORDER BY sol.item 


-- Consulta


SELECT sol0.id SolicNo,sol.id id,substring(to_char(sol0.fecha,'yyyy-mm-dd'),1,10)  fecha,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,
sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,
 est.nombre estValidacion, sol."estadosValidacion_id" estadosValidacion_id , usu.nom_usuario usuSolicitud
FROM public.solicitud_solicitudes sol0
LEFT JOIN public.solicitud_solicitudesDetalle sol ON (sol.solicitud_id  = sol0.id )
LEFT JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id )
LEFT JOIN public.solicitud_tiposcompra tip ON ( tip.id = sol."tiposCompra_id")
LEFT JOIN public.solicitud_presentacion pres ON (pres.id = sol.presentacion_id)
LEFT JOIN public.mae_articulos art     ON (art.codreg_articulo = sol.producto )
LEFT JOIN public.solicitud_usuarios usu ON (usu.id = sol0."usuarios_id")
LEFT JOIN public.solicitud_estadosvalidacion est     ON (est.id = sol."estadosValidacion_id" )
 WHERE sol0.fecha >= '2001-01-01T00:00' and sol0.fecha <= '2023-03-22T00:00'  and usu.num_identificacion = '1013605270' 
 ORDER BY sol0.fecha, sol.item

select * from solicitud_solicitudesdetalle;
select * from solicitud_solicitudes;
select * from solicitud_usuarios;


-- Compras

SELECT sol0.id solicitudNo,to_char(sol0.fecha,'YYYY - MM - DD HH: MM.SS') fecha, sol0.area_id area, areas.area nombre_area, sol0.usuarios_id idUsuarioCreaSol , usuariosCreaSol.nom_usuario usuariosCreaSol,
sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,
pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,usu.nom_usuario usuResp  , est.nombre estValidacion,
est1.nombre estadosAlmacen, sol."estadosValidacion_id" estadosValidacion_id, sol."especificacionesAlmacen" especificacionesAlmacen, 
sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen , sol."observacionesCompras" observacionesCompras, 
sol."estadosCompras_id" estadosCompras_id, est2.nombre estadosCompras, usu2.nom_usuario usuCompras  
FROM public.solicitud_solicitudes sol0 
INNER JOIN public.solicitud_solicitudesDetalle sol ON (sol.solicitud_id = sol0.id)
INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id )
 INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) 
INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id) 
INNER JOIN public.mae_articulos art   ON (art.codreg_articulo = sol.producto) 
LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") 
LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") 
LEFT JOIN public.solicitud_usuarios usu2 ON (usu2.id = sol."usuarioResponsableCompra_id")
 INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) 
INNER JOIN public.solicitud_estadosvalidacion est1  ON (est1.id = sol."estadosAlmacen_id")  
INNER JOIN public.solicitud_estadosvalidacion est2  ON (est2.id = "estadosCompras_id")
inner join public.solicitud_areas areas on (areas.id = sol0.area_id) 
inner join public.solicitud_usuarios usuariosCreaSol on (usuariosCreaSol.id = sol0.usuarios_id) 
WHERE  sol0.estadoReg = 'A' AND sol."estadosCompras_id" = 1
ORDER BY sol.item 


--
SELECT sol0.id solicitudNo,to_char(sol0.fecha,'YYYY-MM-DD HH: MM.SS') fecha, sol0.area_id area, areas.area nombre_area, sol0.usuarios_id idUsuarioCreaSol , usuariosCreaSol.nom_usuario usuariosCreaSol, 
sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,
pres.nombre presentacion,sol.cantidad, sol.justificacion  , sol."especificacionesTecnicas" tec,usu.nom_usuario usuResp  , 
est.nombre estValidacion,est1.nombre estadosAlmacen, sol."estadosValidacion_id" estadosValidacion_id, sol."especificacionesAlmacen" especificacionesAlmacen, 
sol."estadosAlmacen_id" estadosAlmacen_id ,   usu1.nom_usuario usuAlmacen , sol."observacionesCompras" observacionesCompras, 
sol."estadosCompras_id" estadosCompras_id, est2.nombre estadosCompras, usu2.nom_usuario usuCompras , sol."adjuntoCompras"  adjuntoCompras  
FROM public.solicitud_solicitudes sol0 
INNER JOIN public.solicitud_solicitudesDetalle sol ON (sol.solicitud_id = sol0.id) 
INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) 
INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) 
INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id)  
INNER JOIN public.mae_articulos art ON (art.codreg_articulo = sol.producto) 
LEFT JOIN public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id")  
LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") 
LEFT JOIN public.solicitud_usuarios usu2 ON (usu2.id = sol."usuarioResponsableCompra_id")  
INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) 
INNER JOIN public.solicitud_estadosAlmacen est1 ON (est1.id = sol."estadosAlmacen_id") 
INNER JOIN public.solicitud_estadosvalidacion est2 ON (est2.id = "estadosCompras_id") 
inner join public.solicitud_areas areas on (areas.id = sol0.area_id) 
inner join public.solicitud_usuarios usuariosCreaSol on (usuariosCreaSol.id = sol0.usuarios_id) 
WHERE sol0.estadoReg = 'A' AND sol. "estadosCompras_id" = 1 ORDER BY sol.item

----  compraS

SELECT sol.id id,sol.item item, sol.descripcion_id, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,pres.nombre presentacion, sol."solicitadoAlmacen" solicitadoAlmacen,sol.iva iva ,sol."recibidoOrdenCantidad" recibidoOrdenCantidad,sol."recibidoOrdenValor" recibidoOrdenValor,sol."solicitadoOrdenCantidad" solicitadoOrdenCantidad,sol."solicitadoOrdenValor" solicitadoOrdenValor,sol."valorUnitario" valorUnitario 
FROM public.solicitud_solicitudesDetalle sol 
INNER JOIN  public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id) 
INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id") 
INNER JOIN public.solicitud_presentacion pres ON (pres.id = sol.presentacion_id) 
INNER JOIN public.mae_articulos art   ON (art.codreg_articulo = sol.producto) 
LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") 
LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id" ) 
LEFT JOIN public.solicitud_usuarios usu2 ON (usu2.id = sol."usuarioResponsableCompra_id" ) 
INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id") 
INNER JOIN public.solicitud_estadosAlmacen est1 ON (est1.id = sol."estadosAlmacen_id") 
INNER JOIN public.solicitud_estadosvalidacion est2  ON (est2.id = "estadosCompras_id") 
WHERE sol.solicitud_id = 7 AND est2.nombre like ('%APROBA%')  AND  (sol."ordenCompra_id"= 0 OR  sol."ordenCompra_id" is null) 
 ORDER BY sol.item

select * from solicitud_usuarios;
select * from solicitud_areas;

select sol.usuarios_id idSol, usu.nom_usuario usuSolicita,usu1.nom_usuario usuCompras, usu1.nom_usuario respCompras, areas.area area
from solicitud_solicitudes sol
inner join solicitud_solicitudesdetalle sol0 ON (sol0.solicitud_id = sol.id)
inner join solicitud_areas areas on (areas.id = sol.area_id)
inner join solicitud_usuarios usu on (usu.id = sol.usuarios_id)
inner join solicitud_usuarios usu1 on (usu1.id = sol0."usuarioResponsableCompra_id")
where sol.id = 9 limit 1

select * from solicitud_ordenescompra;

,proveedor proveedor, area.area, usu.nom_usuario usuarioCompras,  usu1.nom_usuario usuarioAproboStaff

-- Ordenes de Compra

select ord.id id, substring(to_char(ord."fechaElab",'yyyy-mm-dd'),1,10) fechaElab, ord."estadoOrden" estadoOrden ,ord.opciones opciones,ord."valorBruto" valorBruto,
ord."descuento" descuento,ord."valorParcial" valorParcial, ord."iva" iva, ord."valorTotal" valorTotal,ord.observaciones observaciones,ord.area_id area,
 ord.proveedor_id proveedor,sol.item item,art.articulo, sol.iva iva,sol."recibidoOrdenCantidad" recibidoOrdenCantidad,
sol."solicitadoOrdenCantidad" solicitadoOrdenCantidad ,sol."valorUnitario" valorUnitario	, sol."solicitadoOrdenValor" solicitadoOrdenValor,
sol."recibidoOrdenValor" recibidoOrdenValor ,proveedor proveedor, area.area, usu.nom_usuario usuarioCompras,  usu1.nom_usuario usuarioAproboStaff

FROM solicitud_ordenesCompra ord
INNER JOIN solicitud_solicitudesdetalle sol ON (sol."ordenCompra_id" = ord.id)
INNER JOIN mae_articulos art ON ( art.codreg_articulo = sol.producto)
INNER JOIN solicitud_proveedores prov on (prov.id = ord.proveedor_id)
INNER JOIN solicitud_areas area on (area.id = ord.area_id)
INNER JOIN solicitud_usuarios usu on (usu.id = ord."responsableCompra_id")
INNER JOIN solicitud_Staff usu1 on (usu1.id = ord."aproboCompraStaff_id")
WHERE ord."fechaElab" >= '2023-01-01' and ord."fechaElab" <= '2023-03-27' 
ORDER BY ord."fechaElab", sol.item
  


select * from solicitud_solicitudes;
select * from solicitud_solicitudesdetalle where  solicitud_id =  19;

select sol.usuarios_id idSol, sol.usuarios_id usuSolicita,sol0."usuarioResponsableCompra_id" usuCompras, sol0."usuarioResponsableCompra_id" respCompras, 
areas.id area 
from solicitud_solicitudes sol 
inner join solicitud_solicitudesdetalle sol0 ON (sol0.solicitud_id = sol.id) 
inner join solicitud_areas areas on (areas.id = sol.area_id) 
inner join solicitud_usuarios usu on (usu.id = sol.usuarios_id) 
inner join solicitud_usuarios usu1 on (usu1.id = sol0."usuarioResponsableCompra_id") 
where sol.id = 18 limit 1