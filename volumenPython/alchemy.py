#pip install sqlalchemy
from sqlalchemy import create_engine

#engine = create_engine("apacheimpala://?Server=kudu-impala&Port=21050")
engine = create_engine("hive://kudu-impala:21050/default")
conn = engine.connect()

query = 'select * from impala_user_ratings_as_select limit 50;'
result = conn.execute(query)
print(result.fetchall())