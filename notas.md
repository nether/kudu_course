# Curso Apache Kudu

## Chat del Curso

<https://us02web.zoom.us/j/81041392975?pwd=YUdXVmFhY3hqVFhPQWhFUy91dVNLZz09>

## Documentación

Databricks: <https://drive.google.com/file/d/1H2Wj15fSHZ5h8PxJz97j7T5UzUuJhoZy/view>
Apache Kudu: <https://drive.google.com/file/d/1WgXo6BxfKlhbBRiGdQP8V98mpNhx7FXk/view>
Temario: <https://sixgroup-my.sharepoint.com/personal/jorge_fernandez2_six-group_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fjorge%5Ffernandez2%5Fsix%2Dgroup%5Fcom%2FDocuments%2FAnlagen%2FFormacio%CC%81n%20en%20Big%20Data%20con%20Apache%20Kudu%20%2D%20Aula%20Virtual%20en%20Directo%2Epdf&parent=%2Fpersonal%2Fjorge%5Ffernandez2%5Fsix%2Dgroup%5Fcom%2FDocuments%2FAnlagen>
Big Data Sesión 2: <https://drive.google.com/file/d/1ZxGfeViytrIn1ev_AlBoRM0k7k_m5oHF/view>

## Arrancar KUDU

Establecer variable de entorno en Powershell => $env:KUDU_QUICKSTART_IP=10.144.10.153
Establecer variable de entorno en CMD => set KUDU_QUICKSTART_IP=10.144.10.153
docker-compose -f docker/quickstart.yml up -d
<http://localhost:8050/>

## Contenedor Impala

docker run -d --name kudu-impala --network="docker_default" -p 21000:21000 -p 21050:21050 -p 25000:25000 -p 25010:25010 -p 25020:25020 --memory=4096m apache/kudu:impala-latest impala
docker exec -it kudu-impala impala-shell
Si el comando anterior nos deja la consola desconectada hay que ejecutar el commando `connect;`

Comando para ver las Bases de Datos: `show databases;`
Comando para ver las tablas en la BBDD: `show tables;`

Creación de una tabla desde Impala:

```SQL
CREATE TABLE primeratabla
(
    id BIGINT,
    name STRING,
    PRIMARY KEY(id)
)
PARTITION BY HASH PARTITIONS 4
STORED AS KUDU;
```
