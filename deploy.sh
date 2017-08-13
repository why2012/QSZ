#!/bin/bash
# docker run -d -v /QSZ/mysqldata:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=qingsongzumysqlserver2017. --name mysql-server daocloud.io/library/mysql
# sudo docker run -it -d -v /:/workdir -p 20001:20001 -p 20002:20002 --name tornado-env tornado-env:0.1 bash -c "cd /workdir/QSZ/QSZ && chmod a+x deploy.sh && ./deploy.sh online"
case "$@" in
	online)
		sed -i "s/DEV = True/DEV = False/g" conf/Config.py
		sed -i 's/"debug": True/"debug": False/g' Setting.py
		python MainApplication.py
		;;
	dev-deploy)
		ssh -t why@119.29.113.28 "bash -c 'cd /QSZ/QSZ && git branch && git stash && git pull && sudo docker restart tornado-env'"
		;;
	online-deploy)
		ssh -t why@119.29.113.28 "bash -c 'cd /QSZ/QSZ && git checkout master && git branch && git stash && git pull && sudo docker restart tornado-env'"
		;;
	rollback)
		ssh -t why@119.29.113.28 "bash -c 'cd /QSZ/QSZ && git reset --hard HEAD^ && sudo docker restart tornado-env'"
		;;
	*)
		echo "dev-deploy online-deploy rollback"
		;;
esac