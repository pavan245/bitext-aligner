import db.mysql_connection as connection

conn = connection.get_new_mysql_connection()

print(conn.charset)
print('isConnected :: ', conn.is_connected())

conn.close()

