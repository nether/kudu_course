# pip install impyla
from impala.dbapi import connect
import csv

#pip install pandas
import pandas
from impala.util import as_pandas

def execute_query(conn, query):
    try:
        
        print('Conectado a Impala')
        cursor = conn.cursor()
        cursor.execute(query)
        resultado = cursor.fetchall()
        cursor.close()

        return resultado
    except Exception as ex:
        print(ex)

def create_csv(result):
    csv_file = '/tmp/users/items_export.csv'    

    with open(csv_file, 'w') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
        for item in result:
            csv_writer.writerow(item)

def print_result(result):
    for item in result:
        print(item)

def use_panda_ds(impala_conn, query):
    pandas_cursor = impala_conn.cursor() 
    pandas_cursor.execute(query) 
    pandas_df = as_pandas(pandas_cursor)     
    print('************************ PANDAS DF ***************************' )
    print(pandas_df.head(10))


impala_conn = connect(host='kudu-impala', port=21050)
query = 'select * from impala_user_ratings_as_select limit 50;'
result = execute_query(impala_conn, query)
print_result(result)
create_csv(result)
print('')
print('')
use_panda_ds(impala_conn, query)


