cd `dirname $0`
target_dir=`pwd`

pid=`ps ax | grep -i 'App.py' | grep ${target_dir} | grep python3 | grep -v grep | awk '{print $1}'`
if [ -z "$pid" ] ; then
        echo "No idcardOrcServer running."
        exit -1;
fi

echo "The idcardOrcServer(${pid}) is running..."

kill -9 ${pid}

echo "Send shutdown request to idcardOrcServer(${pid}) OK"