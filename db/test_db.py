import db.mysql_connection as connection
import db.constants as const

conn = connection.get_new_mysql_connection(const.DB_CONFIG_FILE)

print('MySQL Server version :: ', conn.get_server_info())
print('isConnected :: ', conn.is_connected())

conn.close()

