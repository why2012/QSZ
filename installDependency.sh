#!/bin/bash
case "$@" in
	install) 
		sudo pip install -i https://pypi.tuna.tsinghua.edu.cn/simple MySQL-python tornado numpy binascii
		sudo pip install pycrypto
	;;
	start)
		sudo /Applications/XAMPP/bin/mysql.server start
	;;
	stop)
		sudo /Applications/XAMPP/bin/mysql.server stop
	;;
	*)
		echo "install; start; stop"
	;;
esac	