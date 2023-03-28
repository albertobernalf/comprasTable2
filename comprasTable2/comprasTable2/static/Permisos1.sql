---------------------------------------
-- Permisos para Asignar en Produccion
---------------------------------------
 
----------------------------------------------------------------
-- revoke all privileges on database postgres from public; Nop Bloquea los usaurios
----------------------------------------------------------------

---------------------------------------
-- role 0. admin,, Hay que crear imhotep = admin / odbc = consulta / desarrollo = desarrollo
--------------------------------------- 

reassign owned by admin to postgres;
drop owned by admin;
drop ROLE admin; 

CREATE ROLE admin  NOSUPERUSER CREATEDB CREATEROLE NOINHERIT LOGIN ;
ALTER ROLE admin WITH PASSWORD '123';
GRANT CONNECT ON DATABASE bd_imhotep TO admin;
GRANT CONNECT ON DATABASE hiruko TO admin;
GRANT CONNECT ON DATABASE bd_solicitudes_imhotep TO admin;
GRANT USAGE ON SCHEMA public TO admin;
GRANT ALL ON ALL TABLES IN SCHEMA public TO admin;
--grant all privileges on database postgres to facturacion;

---------------------------------------
-- ROLE 1. imhotep
---------------------------------------

reassign owned by imhotep to postgres;
drop owned by imhotep;
drop ROLE imhotep;

CREATE ROLE imhotep  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE imhotep WITH PASSWORD '123'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
REVOKE CONNECT ON DATABASE bd_capacitaciones_2022 FROM PUBLIC;
--REVOKE CONNECT ON DATABASE bd_solicitudes_imhotep FROM PUBLIC;
GRANT CONNECT ON DATABASE bd_imhotep TO imhotep;
GRANT CONNECT ON DATABASE hiruko TO imhotep;
GRANT CONNECT ON DATABASE bd_solicitudes_imhotep TO imhotep;

GRANT USAGE ON SCHEMA public TO imhotep;
GRANT ALL  ON ALL TABLES IN SCHEMA public   TO imhotep;

-- OJO FALTA REVOCAR DROP TABLE

---------------------------------------
-- ROLE 2. Desarrollo
---------------------------------------

reassign owned by desarrollo to postgres;
drop owned by desarrollo;
drop ROLE desarrollo;


CREATE ROLE desarrollo  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE desarrollo WITH PASSWORD '123';
GRANT USAGE ON SCHEMA public TO desarrollo;
GRANT CONNECT ON DATABASE bd_imhotep TO desarrollo;
GRANT ALL ON ALL TABLES IN SCHEMA public TO desarrollo;
-- grant all privileges on database postgres to desarrollo;
--

---------------------------------------
-- ROLE 3. glosas
---------------------------------------


reassign owned by glosas to postgres;
drop owned by glosas;
drop ROLE glosas;


CREATE ROLE glosas  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE glosas WITH PASSWORD '123'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
GRANT CONNECT ON DATABASE bd_imhotep TO glosas;
GRANT USAGE ON SCHEMA public TO glosas;
GRANT SELECT   ON ALL TABLES IN SCHEMA public   TO glosas;
alter user glosas set default_transaction_read_only=on;

 
----------------------------------------
-- ROLE 3.5 facturacion  PRODUCCION
----------------------------------------

reassign owned by facturacion to postgres;
drop owned by facturacion;
drop ROLE facturacion;


CREATE ROLE facturacion  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE facturacion WITH PASSWORD '123'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
GRANT CONNECT ON DATABASE bd_imhotep TO facturacion;
GRANT USAGE ON SCHEMA public TO facturacion;
GRANT SELECT   ON ALL TABLES IN SCHEMA public   TO facturacion;
alter user facturacion set default_transaction_read_only=on;

----------------------------------------
-- FIN ROLE 3.5 facturacion  PRODUCCION
----------------------------------------

---------------------------------------
-- ROLE 4. analistasi
---------------------------------------

reassign owned by analistasi to postgres;
drop owned by analistasi;
drop ROLE analistasi;


CREATE ROLE analistasi  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE analistasi WITH PASSWORD '123'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
GRANT CONNECT ON DATABASE bd_imhotep TO analistasi;
GRANT USAGE ON SCHEMA public TO analistasi;
GRANT SELECT   ON ALL TABLES IN SCHEMA public   TO analistasi;
alter user analistasi set default_transaction_read_only=on;

---------------------------------------
-- ROLE 5. lidersi
---------------------------------------

reassign owned by lidersi to postgres;
drop owned by lidersi;
drop ROLE lidersi;


CREATE ROLE lidersi  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE lidersi WITH PASSWORD '123'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
GRANT CONNECT ON DATABASE bd_imhotep TO lidersi;
GRANT USAGE ON SCHEMA public TO lidersi;
GRANT SELECT  ON ALL TABLES IN SCHEMA public   TO lidersi;
alter user lidersi set default_transaction_read_only=on;

 
 
---------------------------------------
-- ROLE 6. capacitaciones
----------- ----------------------------
 

reassign owned by capacitaciones to postgres;
drop owned by capacitaciones;
drop ROLE capacitaciones;
 

CREATE ROLE capacitaciones  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE capacitaciones WITH PASSWORD '123'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
GRANT CONNECT ON DATABASE bd_capacitaciones_2022 TO capacitaciones;
GRANT CONNECT ON DATABASE hiruko TO capacitaciones;
GRANT CONNECT ON DATABASE bd_solicitudes_imhotep TO capacitaciones;

GRANT USAGE ON SCHEMA public TO capacitaciones;
GRANT all   ON ALL TABLES IN SCHEMA public   TO capacitaciones;
GRANT ALL ON DATABASE bd_capacitaciones_2022 TO capacitaciones;

--alter user glosas set default_transaction_read_only=on;
 
-- Procedimiento IMPLEMENTACION SISTEMA DE SEGURIDAD BASE DE DATOS:

Ejercicio Abril 11 de 2022

En pruebas :

Se valida pg_hba.conf, postgresql.conf, en pruebas estan ok

Se copia backup de produccion a pruebas bd_imhotep

Se crean los ROLES : imhotep / pero parece que los Roles ya estan en la base de datos de pruebas

Se crea base de datos bd_imhotep conmo dueño imhotep y se restaura

Se crea base de datos bd_solicitudes_imhotep conmo dueño imhotep y se restaura

Se crean los ROLES : capacitaciones

Se crea base de datos capacitaciones_2022 como dueño capacitaciones y se restaura. OJO esta vez el dueño fue imhotepo hay que vaklidar esto

Se crean los ROLES : glosas, desarrollo, analistasi, lideresi, admin

-- Esta parte solo para PRODUCCION - ONLINE

-- En produccion, adicionalmente :

-- Se deb copiar el archivo pg_hba.conf de pruebas
 
-- Se crea bases de datos bd_imhotep como dueño imhotep y se restaura

-- Base de datos hiruko se deja tal cual ..

-- Ojo pendientes ademas Reiniciar el Postgres para que tomo los ultimos valores Actualizados


-- Probat Aplicativos en pruebas : 

-- pregguntas : Que pasa si se borrarn las bases de datos ? Es necsario volver a crear ROLES ???. Verificar en el CLUSTER que los ROLES este activos, dependiendo de esto se crean o no

-- Ojo probar backups tipo TAR desde POSTGRES, y descomprimir :  tar -cvf filename.tar files/directories



---------------------------------------
-- ROLE 3. consulta
---------------------------------------


reassign owned by consulta to postgres;
drop owned by consulta;
drop ROLE consulta;


CREATE ROLE consulta  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE consulta WITH PASSWORD '123'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
GRANT CONNECT ON DATABASE bd_imhotep TO consulta;
GRANT USAGE ON SCHEMA public TO consulta;
GRANT SELECT   ON ALL TABLES IN SCHEMA public   TO consulta;
alter user consulta set default_transaction_read_only=on;


---------------------------------------
-- ROLE 3. powerbi Produccion
---------------------------------------


reassign owned by powerbi to postgres;
drop owned by powerbi;
drop ROLE powerbi;


CREATE ROLE powerbi  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE powerbi WITH PASSWORD 'powerbi'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
GRANT CONNECT ON DATABASE bd_imhotep TO powerbi;
GRANT USAGE ON SCHEMA public TO powerbi;
GRANT SELECT   ON ALL TABLES IN SCHEMA public   TO powerbi;

alter user powerbi set default_transaction_read_only=on;
--alter user powerbi set default_transaction_read_only=off;

GRANT SELECT ON v_censo TO powerbi;
GRANT ALL PRIVILEGES ON v_PRUEBAS TO powerbi;
create or replace view v_PRUEBAS AS SELECT * FROM MAE_CAMAS WHERE CODREG_CAMA='0';
select * from v_PRUEBAS;

---------------------------------------
-- ROLE 3, powerbi pero para pruebas de tal forma que pueda crear vistas : bd_imhotep
---------------------------------------

reassign owned by powerbi to postgres;
drop owned by powerbi;
drop ROLE powerbi;


CREATE ROLE powerbi  NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN ;
ALTER ROLE powerbi WITH PASSWORD 'powerbi'; -- Hasta aqui deja conectar a cualquier base de datos
-- deja crear y borra tablas
GRANT CONNECT ON DATABASE bd_imhotep TO powerbi;
GRANT USAGE ON SCHEMA public TO powerbi;
--GRANT SELECT   ON ALL TABLES IN SCHEMA public   TO powerbi;
grant all privileges on database bd_imhotep  to powerbi;


ALTER TABLE v_censo OWNER TO powerbi;
select * from v_censo;





 