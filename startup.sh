export BASE_DIR=`cd $(dirname $0)/; pwd`


if [ ! -d "${BASE_DIR}/logs" ]; then
  mkdir ${BASE_DIR}/logs
fi

# check the start.out log output file
if [ ! -f "${BASE_DIR}/logs/start.out" ]; then
  touch "${BASE_DIR}/logs/start.out"
fi


nohup python3 /www/wwwroot/oisp/idcard-ocr/App.py >> ${BASE_DIR}/logs/start.out 2>&1 &
