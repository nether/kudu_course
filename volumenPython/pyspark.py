from pyspark.sql import SparkSession

if __name__ == '__main':
    spark = SparkSession \
        .builder \
        .master("local") \
        .enableHiveSupport() \
        .appName("kuduapp-vuelos") \
        .config("spark.driver.memory","1g") \
        .getOrCreate()
    spark.sql("CREATE TEMPORARY VIEW FLIGHTS USING parquet OPTIONS (path 'data/flightime.parquet')")
    df = spark.sql("""
        SELECT FL_DATE DATE,
        OP_CARRIER88
    """)

