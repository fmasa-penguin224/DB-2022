FROM mysql
ADD ./start /docker-entrypoint-initdb.d
