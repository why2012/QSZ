#!/bin/bash
# docker run -d -v /QSZ/mysqldata:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=qingsongzumysqlserver2017. --name mysql-server daocloud.io/library/mysql
# sudo docker run -it -d -v /:/workdir -p 20001:20001 -p 20002:20002 --name tornado-env tornado-env:0.1 bash -c "cd /workdir/QSZ/QSZ && ./deploy online"
case "$@" in
	online)
		sed -i "s/DEV = True/DEV = False/g" conf/Config.py
		python MainApplication.py
		;;
	*)
		ssh -t ssh why@119.29.113.28 "bash -c 'cd /QSZ/QSZ && git stash && git pull && sudo docker restart tornado-env'"
		;;
esac