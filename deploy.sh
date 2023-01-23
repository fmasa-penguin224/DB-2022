

#!/bin/bash

docker-compose down
#docker-compose down --rmi all --volumes --remove-orphans

rm -r -f ./mysql

docker-compose build

#docker build ./python -t shomaigu/mysql-database-class:latest .
#docker push shomaigu/mysql-database-class

docker-compose up
