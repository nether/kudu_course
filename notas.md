# Curso Apache Kudu

## Chat del Curso

<https://us02web.zoom.us/j/81041392975?pwd=YUdXVmFhY3hqVFhPQWhFUy91dVNLZz09>

## Documentación

Databricks: <https://drive.google.com/file/d/1H2Wj15fSHZ5h8PxJz97j7T5UzUuJhoZy/view>

Apache Kudu: <https://drive.google.com/file/d/1WgXo6BxfKlhbBRiGdQP8V98mpNhx7FXk/view>

Temario: <https://sixgroup-my.sharepoint.com/personal/jorge_fernandez2_six-group_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fjorge%5Ffernandez2%5Fsix%2Dgroup%5Fcom%2FDocuments%2FAnlagen%2FFormacio%CC%81n%20en%20Big%20Data%20con%20Apache%20Kudu%20%2D%20Aula%20Virtual%20en%20Directo%2Epdf&parent=%2Fpersonal%2Fjorge%5Ffernandez2%5Fsix%2Dgroup%5Fcom%2FDocuments%2FAnlagen>

Big Data Sesión 2: <https://drive.google.com/file/d/1ZxGfeViytrIn1ev_AlBoRM0k7k_m5oHF/view>

## Arrancar KUDU

Establecer variable de entorno en Powershell => `$env:KUDU_QUICKSTART_IP="10.144.10.153"`

Establecer variable de entorno en CMD => `set KUDU_QUICKSTART_IP=10.144.10.153`

`docker-compose -f docker/quickstart.yml up -d`

<http://localhost:8050/>

## Contenedor Impala

Descarga y arranque de imagen Apache Impala: `docker run -d --name kudu-impala --network="docker_default" -p 21000:21000 -p 21050:21050 -p 25000:25000 -p 25010:25010 -p 25020:25020 --memory=4096m apache/kudu:impala-latest impala`

Entrar en la consola de impala dentro del docker: `docker exec -it kudu-impala impala-shell`

Si el comando anterior nos deja la consola desconectada hay que ejecutar el commando `connect;`

Copiar ficheros al docker: `docker cp C:\GIT\Utils\cursoApacheKudu\user_ratings.txt f5273b3d3531:/tmp/user_ratings.txt`

Comando para ver las Bases de Datos: `show databases;`
Comando para ver las tablas en la BBDD: `show tables;`

### Creación de una tabla desde Impala

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

### Insercción de datos

```SQL
INSERT INTO primeratabla VALUES (1,"juan");
INSERT INTO primeratabla VALUES (2,"maria"), (3,"javier"), (4,"alberto");
```

### Selección de datos

```SQL
SELECT * from primeratabla;
```

### Update

```SQL
UPDATE primeratabla SET name="pedro" WHERE id=2;
```

### Insert + Update

```SQL
UPSERT INTO primeratabla VALUES (2,"marta"), (5,"raul");
```

### Borrado

```SQL
DELETE FROM primeratabla WHERE id>3;
```

Creación de una tabla externa linkada a otra tabla

```SQL
CREATE EXTERNAL TABLE segundatabla STORED AS KUDU
TBLPROPERTIES('kudu.table_name' = 'impala::default.primeratabla');
```

### Descripción de los campos de una tabla

```SQL
describe primeratabla;
```

### Borrado de tablas

```SQL
drop table primeratabla;
```

### Creación de una table en Impala con datos de un fichero

```SQL
DROP TABLE IF EXISTS user_item_ratings;
DROP TABLE IF EXISTS kudu_user_ratings;
DROP TABLE IF EXISTS kudu_user_ratings_as_select;

CREATE EXTERNAL TABLE user_item_ratings
(
ts INT,
userid INT,
movieid INT,
rating INT,
age INT,
gender STRING,
occupation STRING,
zip INT,
movietitle STRING,
releasedate STRING,
videoreleasedate STRING,
url STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\001' STORED AS TEXTFILE LOCATION '/tmp/users/';
```

### Creación de una tabla en Kudu

Se crea usando una PrimeryKey de 2 campos y un hash de un solo campo (el campo del hash debe ser uno de los del primaryKey)

```SQL
CREATE TABLE kudu_user_ratings (
    movieid INT,
    userid INT,
    rating INT,
    age INT,
    gender STRING,
    occupation STRING,
    zip INT,
    movietitle STRING,
    releasedate STRING,
    videoreleasedate STRING,
    url STRING,
    ts INT,
    PRIMARY KEY(movieid,userid)    
)
PARTITION BY HASH(movieid)
PARTITIONS 4 STORED AS KUDU;

INSERT INTO kudu_user_ratings SELECT movieid, userid, rating, age,gender, occupation, zip, movietitle, releasedate, videoreleasedate, url, ts FROM user_item_ratings;

CREATE TABLE kudu_user_ratings_as_select PRIMARY KEY(movieid,userid) PARTITION BY HASH(movieid) PARTITIONS 4 STORED AS KUDU AS SELECT movieid, userid, rating, age, gender, occupation, zip, movietitle, releasedate, videoreleasedate, url, ts  FROM user_item_ratings;
```

### Consultas

```SQL
SELECT userid, minimum_rating, maximum_rating, total 
FROM (    
    SELECT userid AS user, 
            MIN(rating) AS minimum_rating,        
            MAX(rating) as maximum_rating    
    FROM        user_item_ratings    
    GROUP BY        userid    
    ) AS minmax_ratings 
    JOIN (    
        SELECT  userid,
                count(*) AS total    
        FROM        user_item_ratings    
        GROUP BY        userid    ) AS totalratings 
    ON    minmax_ratings.user=totalratings.userid 
    ORDER BY    total DESC LIMIT 10;

SELECT COUNT(*), AVG(rating) FROM user_item_ratings WHERE movieid=470 AND userid=276;

SELECT AVG(rating) FROM kudu_user_ratings WHERE movietitle='Tombstone (1993)';
```

## Particionado HASH

Particionado HASH -> Módulo del número de particiones
Número fijo de Buckets
Se distribuye todo el contenido de forma equitativa entre buckets
Las lecturas se paralelizan entre las particiones (a no ser que se pueda saber directamente cual de ellas contiene el dato)
NO SE PUEDEN CREAR BUCKETS A POSTERIORI.

## Particionado RANGE

El rango se especifica durante la creación de la tabla y se mapea con uno o varios valores de la clave primaria.
Es posible añadir o borrar nuevas particiones con un ALTER TABLE.

### Particionando por TIME RANGE

El uso más común de una partición range es usar un campo con fecha para ir haciendo particiones por día o rango de fechas.

## Partición combinada

Se puede combinar la partición de Hash y rango por tiempo para tener una matriz de particiones.

## Cliente Python

Para arrancar una imagen con python y Kudu: `docker run -it --name kudu-python -v C:\Git\Utils\cursoApacheKudu\volumenPython:/clientepython --network docker_default apache/kudu:kudu-python-1.16 bash`

Ver el código de volumenPython/app_v1.py y ejecutarlo en el contenedor de Python

Para ver desde Impala los datos introducidos en Python debemos crear un proxy de la tabla Kudu en Impala:

```SQL
CREATE EXTERNAL TABLE impala_tabla_python
STORED AS KUDU
TBLPROPERTIES('kudu.table_name' = 'tabla-python');
```

## Scala

Para entrar en modo pegado `:paste` (CTRL-D para finalizarlo)

```python
val sfmta_raw = spark.sqlContext.read.format("csv")
  .option("header", "true")
  .option("inferSchema", "true")
  .load("avl.csv")

sfmta_raw.printSchema

sfmta_raw.createOrReplaceTempView("sfmta_raw")

spark.sql("SELECT count(*) FROM sfmta_raw").show()
spark.sql("SELECT * FROM sfmta_raw LIMIT 5").show()
```

Pegar tambien el siguiente código

```scala
import org.apache.spark.sql.types._
import org.apache.spark.sql.DataFrame
def setNotNull(df: DataFrame, columns: Seq[String]) : DataFrame = {
  val schema = df.schema
  // Modify [[StructField] for the specified columns.
  val newSchema = StructType(schema.map {
    case StructField(c, t, _, m) if columns.contains(c) => StructField(c, t, nullable = false, m)
    case y: StructField => y
  })
  // Apply new schema to the DataFrame
  df.sqlContext.createDataFrame(df.rdd, newSchema)
}
val sftmta_time = sfmta_raw
  .withColumn("REPORT_TIME", to_timestamp($"REPORT_TIME", "MM/dd/yyyy HH:mm:ss"))
val sftmta_prep = setNotNull(sftmta_time, Seq("REPORT_TIME", "VEHICLE_TAG"))
sftr a_prep.printSchema
sftmta_prep.createOrReplaceTempView("sftmta_prep")
spark.sql("SELECT count(*) FROM sftmta_prep").show()
spark.sql("SELECT * FROM sftmta_prep LIMIT 5").show()


```