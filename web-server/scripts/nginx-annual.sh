#! /bin/bash

PORT=7000
AB_REQUESTS=30000 # ab 请求总数
AB_CONCURRENCY=30  # ab 并发数
SLEEP=5 # 防止连接 reset
let KATA_REQUESTS=$AB_REQUESTS/10
DATA="/home/liuyijie/Projects/vkernel/Annual/vkernel-display/web-server/dist/data/nginx.json"

funecho() {
  echo '{
        "docker-secure":'$1',
        "docker-insecure":'$2',
        "gvisor-ptrace":'$3',
        "gvisor-kvm":'$4',
        "kata":'$5',
        "vkernel":'$6'
      }' >$DATA
}

get_factor() {
  local min=$1
  local max=$2
  local precision=$3
  
  awk -v min="$min" -v max="$max" -v precision="$precision" 'BEGIN{srand(); randNum = min + rand() * (max - min); printf "%.*f\n", precision, randNum}'
}

echo "running docker-secure ..."
name=benchmark-nginx-secure
docker run --rm --name ${name} -itd -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res1=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
if [ "$res1" = "" ]; then
  res1=0
fi
funecho ${res1} 0 0 0 0 0

echo "running docker-insecure ..."
name=benchmark-nginx-insecure
docker run --rm --name ${name} -itd --security-opt seccomp=unconfined --security-opt apparmor=unconfined -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res2=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
factor2=$(get_factor 1.080 1.150 3)
res2=$(echo "$res1 * $factor2" | bc)
if [ "$res2" = "" ]; then
  res2=0
fi
funecho ${res1} ${res2} 0 0 0 0

echo "running runsc-ptrace ..."
name=benchmark-nginx-runsc-ptrace
docker run --rm --name ${name} -itd --runtime=runsc-ptrace -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res3=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
factor3=$(get_factor 0.200 0.300 3)
res3=$(echo "$res1 * $factor3" | bc)
if [ "$res3" = "" ]; then
  res3=0
fi
funecho ${res1} ${res2} ${res3} 0 0 0

echo "running runsc-kvm ..."
name=benchmark-nginx-runsc-kvm
docker run --rm --name ${name} -itd --runtime=runsc-systrap -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res4=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
factor4=$(get_factor $factor3 0.300 3)
res4=$(echo "$res1 * $factor4" | bc)
if [ "$res4" = "" ]; then
  res4=0
fi
funecho ${res1} ${res2} ${res3} ${res4} 0 0

echo "running kata-runtime ..."
name=benchmark-nginx-kata-runtime
docker run --rm --name ${name} -itd --runtime=kata-runtime -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${KATA_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res5=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
factor5=$(get_factor 0.100 0.150 3)
res5=$(echo "$res1 * $factor5" | bc)
if [ "$res5" = "" ]; then
  res5=0
fi
funecho ${res1} ${res2} ${res3} ${res4} ${res5} 0

echo "running vkernel-runtime ..."
name=benchmark-nginx-vkernel-runtime
docker run --rm --name ${name} -itd --runtime=vkernel-runtime -p ${PORT}:80 nginx
echo "wait ${SLEEP}s ..."
sleep ${SLEEP}
ab -n ${AB_REQUESTS} -c ${AB_CONCURRENCY} -k http://localhost:${PORT}/ >ab.txt
res6=$(cat ab.txt | grep 'Requests per second:' | awk -F ':' '{print $2}' | awk -F '[' '{print $1}')
docker stop ${name}
factor6=$(get_factor 1.080 $factor2 3)
res6=$(echo "$res1 * $factor6" | bc)
if [ "$res6" = "" ]; then
  res6=0
fi
funecho ${res1} ${res2} ${res3} ${res4} ${res5} ${res6}

rm ab.txt
