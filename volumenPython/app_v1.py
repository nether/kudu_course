import kudu
from kudu.client import Partitioning
from datetime import datetime


cliente_kudu = kudu.connect(host=["kudu-master-1","kudu-master-2","kudu-master-3"], port=[7051,7151,7251])

# Esquema de datos
builder = kudu.schema_builder()
builder.add_column('key').type(kudu.int64).nullable(False).primary_key()
builder.add_column('ts_val').type(kudu.unixtime_micros).nullable(False).compression('lz4')
schema = builder.build()

#Particionado
partitioning = Partitioning().add_hash_partitions(column_names=['key'], num_buckets=3)

table_name = 'tabla-python9'

# cliente_kudu.create_table(table_name, schema, partitioning)

table = cliente_kudu.table(table_name)

session = cliente_kudu.new_session()

try:
    #op_insert = table.new_insert({'key':1,'ts_val': datetime.utcnow()})
    op_upsert = table.new_upsert({'key':2,'ts_val': datetime.utcnow()})
    op_update = table.new_update({'key':1,'ts_val': datetime.utcnow()})
    op_delete = table.new_delete({'key':2})
    #session.apply(op_insert)
    session.apply(op_upsert)
    session.apply(op_update)
    session.apply(op_delete)
    session.flush()
except kudu.KuduBadStatus as e:
    print(session.get_pending_errors())

scanner = table.scanner()
scanner.add_predicate(table['key'] == 1)

resultado = scanner.open().read_all_tuples()
print(resultado)

