19456950 / Medical2023
1013605270  coord cartera
1234


80760858  "JEISON MOLINA"   VALIDACION
1234


52973594   --CORELLY   COMPRAS
12345

79717519   --"EDWIN JAIR CUBIDES PIRAMANRIQUE"  ALMACEN
1234

select * from solicitud_usuarios;
SELECT id,nom_usuario  FROM public.solicitud_usuarios WHERE estadoReg = 'A' and perfil  = 'S'

select * from solicitud_usuarios WHERE NOM_USUARIO LIKE ('%MOLINA%');
select * from solicitud_solicitudes;	
select * from solicitud_solicitudesdetalle where solicitud_id=28;	
select * from solicitud_estadosvalidacion;

select id id, fecha, fecha, area_id area_id, usuarios_id usuarios_id from solicitud_solicitudes sol0 where sol.usuarios_id = coordinador and fecha >= ? and fecha <= ? order by fecha
select id id, fecha, fecha, area_id area_id, usuarios_id usuarios_id from solicitud_solicitudes sol where sol.usuarios_id = 4 and fecha >= '2023-01-01' and fecha <= '2023-12-31' order by fecha

update solicitud_solicitudesdetalle set "ordenCompra_id"=null where solicitud_id=29;

 

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

SELECT sol0.id solicitudNo,to_char(sol0.fecha,'YYYY - MM - DD HH: MM.SS') fecha,  areas.area area, 
 usuariosCreaSol.nom_usuario usuariosCreaSol, sol.item item, des.nombre descripcion, tip.nombre tipo, sol.producto producto, art.articulo producto, 
pres.nombre  presentacion, sol.cantidad cantidad, sol.justificacion justificacion, sol."especificacionesTecnicas" tec, usu.nom_usuario usuResp,  est.nombre estValidacion
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
WHERE  sol."usuarioResponsableValidacion_id" = 69  and sol0.fecha>= '2023-01-01' and  sol0.fecha<= '2023-12-01'
ORDER BY sol0.fecha,sol0.id, sol.item


WHERE  sol."usuarioResponsableValidacion_id" = ? and sol0.fecha>= ? and  sol0.fecha<= ?
solicitudNo, fecha, area, usuariosCreaSol, item, descripcion, tipo,  producto, art.articulo producto, presentacion,  cantidad, justificacion, tec, usuResp, estValidacion



-- Almacen

SELECT sol0.id solicitudNo,to_char(sol0.fecha,'YYYY - MM - DD HH: MM.SS') fecha,  areas.area area,  usuariosCreaSol.nom_usuario usuariosCreaSol, 
sol.item item, des.nombre descripcion, tip.nombre tipo ,sol.producto producto,  art.articulo nombre_producto ,
pres.nombre presentacion,sol.cantidad cantidad , sol.justificacion justificacion , sol."especificacionesTecnicas" tec, est.nombre estValidacion, 
est1.nombre estadosAlmacen,  sol."especificacionesAlmacen" especificacionesAlmacen,   usu1.nom_usuario usuAlmacen 
FROM public.solicitud_solicitudes sol0 
INNER JOIN public.solicitud_solicitudesDetalle sol on (sol.solicitud_id=sol0.id)
INNER JOIN public.solicitud_descripcioncompra des ON (des.id = sol.descripcion_id ) 
INNER JOIN public.solicitud_tiposcompra tip ON (tip.id = sol."tiposCompra_id" ) 
INNER JOIN public.solicitud_presentacion pres on (pres.id = sol.presentacion_id) 
INNER JOIN public.mae_articulos art   ON (art.codreg_articulo = sol.producto) 
LEFT JOIN  public.solicitud_usuarios usu ON (usu.id = sol."usuarioResponsableValidacion_id") 
LEFT JOIN public.solicitud_usuarios usu1 ON (usu1.id = sol."usuarioResponsableAlmacen_id") 
INNER JOIN public.solicitud_estadosvalidacion est ON (est.id = sol."estadosValidacion_id" ) 
INNER JOIN public.solicitud_estadosalmacen est1  ON (est1.id = sol."estadosAlmacen_id") 
inner join public.solicitud_areas areas on (areas.id = sol0.area_id) 
inner join public.solicitud_usuarios usuariosCreaSol on (usuariosCreaSol.id = sol0.usuarios_id) 
WHERE  sol."usuarioResponsableAlmacen_id" =  6 and sol0.fecha >= '2023-01-01' and sol0.fecha <= '2023-04-30' 
ORDER BY sol0.fecha,sol0.id,sol.item 

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

select ord.id orden, substring(to_char(ord."fechaElab",'yyyy-mm-dd'),1,10) fechaElab,area.area area, usu.nom_usuario usuarioCompras, proveedor proveedor, 
 sol.item item,art.articulo articulo, pre.nombre presenta, sol.iva iva,sol."solicitadoOrdenCantidad" solicitadoOrdenCantidad ,sol."recibidoOrdenCantidad" recibidoOrdenCantidad,sol."valorUnitario" valorUnitario,
 sol."solicitadoOrdenValor" solicitadoOrdenValor,sol."recibidoOrdenValor" recibidoOrdenValor ,
ord."valorBruto" valorBruto,ord."descuento" descuento,ord."valorParcial" valorParcial, ord."iva" iva, ord."valorTotal" valorTotal,
case when ord."estadoOrden" = 'V' then 'Vigente' when ord."estadoOrden" = 'C' then 'caduca' end  estadoOrden ,case when ord.opciones='A' then 'Anticipo' when ord.opciones='N' then 'Noventa dias' when ord.opciones='C' then 'Contra enrega'  end   opciones,ord.observaciones observaciones, usu1.nom_usuario usuarioAproboStaff
FROM solicitud_ordenesCompra ord
INNER JOIN solicitud_solicitudesdetalle sol ON (sol."ordenCompra_id" = ord.id)
INNER JOIN solicitud_articulos art ON ( art."codregArticulo" = sol.producto)
INNER JOIN solicitud_proveedores prov on (prov.id = ord.proveedor_id)
INNER JOIN solicitud_areas area on (area.id = ord.area_id)
INNER JOIN solicitud_usuarios usu on (usu.id = ord."responsableCompra_id")
INNER JOIN solicitud_Staff usu1 on (usu1.id = ord."aproboCompraStaff_id")
INNER JOIN solicitud_descripcioncompra des on (des.id = sol.descripcion_id)
INNER JOIN solicitud_presentacion pre on (pre.id = sol.presentacion_id)
WHERE ord."fechaElab" >= '2023-01-01' and ord."fechaElab" <= '2023-04-27' and ord."responsableCompra_id" =  11
ORDER BY ord."fechaElab", sol.item



orden,fechaElab,area, usuarioCompras,proveedor, item, articulo, presenta, iva, solicitadoOrdenCantidad , recibidoOrdenCantidad, valorUnitario, solicitadoOrdenValor, recibidoOrdenValor ,valorBruto,descuento, valorParcial, iva, valorTotal,  estadoOrden , opciones,observaciones,  usuarioAproboStaff


  
select * from solicitud_articulos;
select * from solicitud_solicitudes;
update solicitud_solicitudesdetalle set "ordenCompra_id" = null  where solicitud_id=29;
select solicitud_id,"ordenCompra_id" from solicitud_solicitudesdetalle where  solicitud_id >=  10;

select sol.usuarios_id idSol, sol.usuarios_id usuSolicita,sol0."usuarioResponsableCompra_id" usuCompras, sol0."usuarioResponsableCompra_id" respCompras, 
areas.id area 
from solicitud_solicitudes sol 
inner join solicitud_solicitudesdetalle sol0 ON (sol0.solicitud_id = sol.id) 
inner join solicitud_areas areas on (areas.id = sol.area_id) 
inner join solicitud_usuarios usu on (usu.id = sol.usuarios_id) 
inner join solicitud_usuarios usu1 on (usu1.id = sol0."usuarioResponsableCompra_id") 
where sol.id = 18 limit 1

SELECT id id, fecha, fecha, area_id area_id, usuarios_id usuarios_id 
from solicitud_solicitudes sol 
WHERE sol.usuarios_id = 4 and fecha >= '2023-01-01' and fecha <= '2023-12-31'
ORDER BY fecha

select * from solicitud_solicitudes;
select * from solicitud_solicitudesdetalle;
select * from solicitud_usuarios;

SELECT sol.id solicitud, sol.fecha fecha, area.area area,  usu.nom_usuario usuarioSolicitud, sol0.item item , des.nombre descripcion, pre.nombre presentacion,
	tipo.nombre tipoCompra, sol0.producto producto ,art.articulo articulo,sol0.cantidad cantidad, est.nombre estado, usucomp.nom_usuario usuarioCompra, "ordenCompra_id" ordenCompra
from solicitud_solicitudes sol 
left join solicitud_solicitudesdetalle sol0 on (sol0.solicitud_id = sol.id)
inner join solicitud_usuarios usu on (usu.id= sol.usuarios_id)
inner join solicitud_areas area on (area.id = sol.area_id)
inner join solicitud_descripcioncompra des on (des.id = sol0.descripcion_id)
inner join solicitud_presentacion pre on (pre.id = sol0.presentacion_id)
inner join solicitud_tiposcompra tipo on (tipo.id = sol0."tiposCompra_id")
inner join mae_articulos art on (art.codreg_articulo = sol0.producto)
inner join solicitud_usuarios usucomp on (usucomp.id= sol0."usuarioResponsableCompra_id")
inner join solicitud_estadosvalidacion est on (est.id = sol0."estadosCompras_id")
WHERE sol.usuarios_id = 4 and sol.fecha >= '2023-01-01' and sol.fecha <= '2023-12-31'
ORDER BY sol.fecha, sol.id

solicitud, fecha, area,usuarioSolicitud, item, descripcion,presentacion, tipoCompra, producto , articulo, cantidad, estado, usuarioCompra,  ordenCompra

SELECT sol.id solicitud, sol.fecha fecha, area.area area,  usu.nom_usuario usuarioSolicitud, sol0.item item , des.nombre descripcion, pre.nombre presentacion,	tipo.nombre tipoCompra, sol0.producto producto ,art.articulo articulo,sol0.cantidad cantidad, est.nombre estado, usucomp.nom_usuario usuarioCompra, "ordenCompra_id" ordenCompra
from solicitud_solicitudes sol  left join solicitud_solicitudesdetalle sol0 on (sol0.solicitud_id = sol.id) inner join solicitud_usuarios usu on (usu.id= sol.usuarios_id)
inner join solicitud_areas area on (area.id = sol.area_id) inner join solicitud_descripcioncompra des on (des.id = sol0.descripcion_id) inner join solicitud_presentacion pre on (pre.id = sol0.presentacion_id)
inner join solicitud_tiposcompra tipo on (tipo.id = sol0."tiposCompra_id") inner join mae_articulos art on (art.codreg_articulo = sol0.producto)
inner join solicitud_usuarios usucomp on (usucomp.id= sol0."usuarioResponsableCompra_id") inner join solicitud_estadosvalidacion est on (est.id = sol0."estadosCompras_id")



SELECT sol.id solicitud, sol.fecha fecha, area.area area,  usu.nom_usuario usuarioSolicitud, sol0.item item , des.nombre descripcion, pre.nombre presentacion, tipo.nombre tipoCompra, 
sol0.producto producto ,art.articulo articulo,sol0.cantidad cantidad, est.nombre estado, usucomp.nom_usuario usuarioCompra, "ordenCompra_id" ordenCompra 
from solicitud_solicitudes sol  
left join solicitud_solicitudesdetalle sol0 on (sol0.solicitud_id = sol.id) 
inner join solicitud_usuarios usu on (usu.id= sol.usuarios_id) 
inner join solicitud_areas area on (area.id = sol.area_id) 
inner join solicitud_descripcioncompra des on (des.id = sol0.descripcion_id) 
inner join solicitud_presentacion pre on (pre.id = sol0.presentacion_id) 
inner join solicitud_tiposcompra tipo on (tipo.id = sol0."tiposCompra_id") 
inner join mae_articulos art on (art.codreg_articulo = sol0.producto) 
inner join solicitud_usuarios usucomp on (usucomp.id= sol0."usuarioResponsableCompra_id") 
inner join solicitud_estadosvalidacion est on (est.id = sol0."estadosCompras_id") 
WHERE sol.usuarios_id = '4' and fecha >= '2023-04-11T00:00' and fecha <= '2023-04-11T00:00' ORDER BY fecha



select * from solicitud_usuarios;

SELECT sol.id solicitud, sol.fecha fecha, area.area area,  usu.nom_usuario usuarioSolicitud, sol0.item item , des.nombre descripcion, pre.nombre presentacion, 
tipo.nombre tipoCompra, sol0.producto producto ,art.articulo articulo,sol0.cantidad cantidad, est.nombre estado, usucomp.nom_usuario usuarioCompra, 
"ordenCompra_id" ordenCompra from solicitud_solicitudes sol  left join solicitud_solicitudesdetalle sol0 on (sol0.solicitud_id = sol.id) 
inner join solicitud_usuarios usu on (usu.id= sol.usuarios_id) inner join solicitud_areas area on (area.id = sol.area_id) 
inner join solicitud_descripcioncompra des on (des.id = sol0.descripcion_id) inner join solicitud_presentacion pre on (pre.id = sol0.presentacion_id) 
inner join solicitud_tiposcompra tipo on (tipo.id = sol0."tiposCompra_id") inner join mae_articulos art on (art.codreg_articulo = sol0.producto) 
inner join solicitud_usuarios usucomp on (usucomp.id= sol0."usuarioResponsableCompra_id") 
inner join solicitud_estadosvalidacion est on (est.id = sol0."estadosCompras_id")
 WHERE sol.usuarios_id = '4' and fecha >= '2023-01-01' and fecha <= '2023-12-31' ORDER BY fecha
        
