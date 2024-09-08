dni_admin="40000000"
clave_admin="ClaveAdmin"
dni_usuario="40000001"
clave_usuario="ClaveUsuario"
clave_usuario2="ClaveUsuario2"
nombre_usuario="Usuario"

# Alta usuario
node index.js alta $dni_admin $clave_admin $dni_usuario $clave_usuario $nombre_usuario 100 20

# Carga
node index.js carga $dni_admin $clave_admin 1000

# Cambio clave
node index.js clave $dni_usuario $clave_usuario $clave_usuario2

# Extraccion
node index.js extraccion $dni_usuario $clave_usuario2 5

# Consulta saldo
node index.js saldo $dni_usuario $clave_usuario2

# Consulta movimientos
node index.js movimientos $dni_admin $clave_admin $dni_usuario 2022 2023
